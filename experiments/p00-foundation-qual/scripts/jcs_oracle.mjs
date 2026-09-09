#!/usr/bin/env node
/* Maintained RFC 8785 oracle wrapper; package is cached outside Git. */
import fs from "node:fs";
const packageRoot = process.env.QUAL_JCS_PACKAGE;
if (!packageRoot) throw new Error("QUAL_JCS_PACKAGE is required");
const { default: canonicalize } = await import(`${packageRoot}/lib/canonicalize.js`);

const input = fs.readFileSync(0, "utf8");
const value = JSON.parse(input);
process.stdout.write(canonicalize(value));
