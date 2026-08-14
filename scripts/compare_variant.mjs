import { pathToFileURL } from "node:url";

const [goldenPath, mutantPath, target, encodedInput] = process.argv.slice(2);
if (!goldenPath || !mutantPath || !target || !encodedInput) {
  throw new Error("Usage: compare_variant.mjs <golden> <mutant> <target> <base64-input>");
}

const functionNames = {
  registration: "validateRegistration",
  shipping: "calculateOrder",
  loan: "evaluateLoan",
};
const functionName = functionNames[target];
if (!functionName) {
  throw new Error(`Unknown target: ${target}`);
}

const input = JSON.parse(Buffer.from(encodedInput, "base64url").toString("utf8"));
const goldenModule = await import(pathToFileURL(goldenPath));
const mutantModule = await import(pathToFileURL(mutantPath));
const golden = goldenModule[functionName](input);
const mutant = mutantModule[functionName](input);

process.stdout.write(JSON.stringify({
  differs: JSON.stringify(golden) !== JSON.stringify(mutant),
  golden,
  mutant,
}));
