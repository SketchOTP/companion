/* Qualification-only VFS fault runner. It is not Companion runtime code. */
#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef struct QualFile {
    sqlite3_file base;
    sqlite3_file *real;
} QualFile;

static sqlite3_vfs *underlying;
static int fault_enabled;
static int fault_crash;
static int fault_count;

static sqlite3_file *real_file(sqlite3_file *file) {
    return ((QualFile *)file)->real;
}

static int qClose(sqlite3_file *file) { sqlite3_file *r = real_file(file); return r->pMethods->xClose(r); }
static int qRead(sqlite3_file *file, void *buf, int amount, sqlite3_int64 offset) { sqlite3_file *r = real_file(file); return r->pMethods->xRead(r, buf, amount, offset); }
static int qWrite(sqlite3_file *file, const void *buf, int amount, sqlite3_int64 offset) { sqlite3_file *r = real_file(file); return r->pMethods->xWrite(r, buf, amount, offset); }
static int qTruncate(sqlite3_file *file, sqlite3_int64 size) { sqlite3_file *r = real_file(file); return r->pMethods->xTruncate(r, size); }
static int qSync(sqlite3_file *file, int flags) {
    sqlite3_file *r = real_file(file);
    if (fault_enabled && fault_count++ == 0) {
        if (fault_crash) _exit(70);
        return SQLITE_IOERR_FSYNC;
    }
    return r->pMethods->xSync(r, flags);
}
static int qFileSize(sqlite3_file *file, sqlite3_int64 *size) { sqlite3_file *r = real_file(file); return r->pMethods->xFileSize(r, size); }
static int qLock(sqlite3_file *file, int lock) { sqlite3_file *r = real_file(file); return r->pMethods->xLock(r, lock); }
static int qUnlock(sqlite3_file *file, int lock) { sqlite3_file *r = real_file(file); return r->pMethods->xUnlock(r, lock); }
static int qReserved(sqlite3_file *file, int *out) { sqlite3_file *r = real_file(file); return r->pMethods->xCheckReservedLock(r, out); }
static int qControl(sqlite3_file *file, int op, void *arg) { sqlite3_file *r = real_file(file); return r->pMethods->xFileControl(r, op, arg); }
static int qSector(sqlite3_file *file) { sqlite3_file *r = real_file(file); return r->pMethods->xSectorSize(r); }
static int qDevice(sqlite3_file *file) { sqlite3_file *r = real_file(file); return r->pMethods->xDeviceCharacteristics(r); }
static int qShmMap(sqlite3_file *file, int page, int size, int extend, void volatile **out) { sqlite3_file *r = real_file(file); return r->pMethods->xShmMap(r, page, size, extend, out); }
static int qShmLock(sqlite3_file *file, int offset, int n, int flags) { sqlite3_file *r = real_file(file); return r->pMethods->xShmLock(r, offset, n, flags); }
static void qShmBarrier(sqlite3_file *file) { sqlite3_file *r = real_file(file); r->pMethods->xShmBarrier(r); }
static int qShmUnmap(sqlite3_file *file, int delete_flag) { sqlite3_file *r = real_file(file); return r->pMethods->xShmUnmap(r, delete_flag); }
static int qFetch(sqlite3_file *file, sqlite3_int64 offset, int amount, void **out) { sqlite3_file *r = real_file(file); return r->pMethods->xFetch(r, offset, amount, out); }
static int qUnfetch(sqlite3_file *file, sqlite3_int64 offset, void *ptr) { sqlite3_file *r = real_file(file); return r->pMethods->xUnfetch(r, offset, ptr); }

static const sqlite3_io_methods methods = {
    3, qClose, qRead, qWrite, qTruncate, qSync, qFileSize, qLock, qUnlock,
    qReserved, qControl, qSector, qDevice, qShmMap, qShmLock, qShmBarrier,
    qShmUnmap, qFetch, qUnfetch
};

static int qOpen(sqlite3_vfs *vfs, const char *name, sqlite3_file *file, int flags, int *out_flags) {
    QualFile *qual = (QualFile *)file;
    qual->real = (sqlite3_file *)((unsigned char *)file + sizeof(QualFile));
    int rc = underlying->xOpen(underlying, name, qual->real, flags, out_flags);
    if (rc != SQLITE_OK) return rc;
    qual->base.pMethods = &methods;
    return SQLITE_OK;
}

static sqlite3_vfs wrapper;

static int exec_sql(sqlite3 *db, const char *sql) {
    char *error = NULL;
    int rc = sqlite3_exec(db, sql, NULL, NULL, &error);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "rc=%d error=%s\n", rc, error ? error : "unknown");
        sqlite3_free(error);
    }
    return rc;
}

int main(int argc, char **argv) {
    if (argc != 4) return 64;
    const char *db_path = argv[1];
    const char *phase = argv[2];
    fault_crash = strcmp(argv[3], "crash") == 0;
    underlying = sqlite3_vfs_find(NULL);
    if (!underlying) return 65;
    memset(&wrapper, 0, sizeof(wrapper));
    wrapper.iVersion = underlying->iVersion;
    wrapper.szOsFile = (int)(sizeof(QualFile) + underlying->szOsFile);
    wrapper.mxPathname = underlying->mxPathname;
    wrapper.zName = "qualfault";
    wrapper.pAppData = underlying;
    wrapper.xOpen = qOpen;
    wrapper.xDelete = underlying->xDelete;
    wrapper.xAccess = underlying->xAccess;
    wrapper.xFullPathname = underlying->xFullPathname;
    wrapper.xDlOpen = underlying->xDlOpen;
    wrapper.xDlError = underlying->xDlError;
    wrapper.xDlSym = underlying->xDlSym;
    wrapper.xDlClose = underlying->xDlClose;
    wrapper.xRandomness = underlying->xRandomness;
    wrapper.xSleep = underlying->xSleep;
    wrapper.xCurrentTime = underlying->xCurrentTime;
    wrapper.xGetLastError = underlying->xGetLastError;
    wrapper.xCurrentTimeInt64 = underlying->xCurrentTimeInt64;
    if (sqlite3_vfs_register(&wrapper, 0) != SQLITE_OK) return 66;
    sqlite3 *db = NULL;
    int rc = sqlite3_open_v2(db_path, &db, SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE, "qualfault");
    if (rc != SQLITE_OK) return 67;
    rc = exec_sql(db, "PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;");
    if (rc == SQLITE_OK && strcmp(phase, "commit") == 0) {
        rc = exec_sql(db, "BEGIN IMMEDIATE; INSERT INTO events(id,payload) VALUES('vfs-commit-fault','synthetic');");
        fault_enabled = rc == SQLITE_OK;
        if (rc == SQLITE_OK) rc = exec_sql(db, "COMMIT;");
    } else if (rc == SQLITE_OK && strcmp(phase, "checkpoint") == 0) {
        rc = exec_sql(db, "BEGIN IMMEDIATE; INSERT INTO events(id,payload) VALUES('vfs-checkpoint-fault','synthetic'); COMMIT;");
        fault_enabled = rc == SQLITE_OK;
        if (rc == SQLITE_OK) rc = exec_sql(db, "PRAGMA wal_checkpoint(TRUNCATE);");
    } else if (rc == SQLITE_OK) {
        rc = 68;
    }
    sqlite3_close(db);
    sqlite3_vfs_unregister(&wrapper);
    return rc == SQLITE_OK ? 0 : 69;
}
