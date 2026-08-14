const MUTANT_TARGETS = Object.freeze({
  M01: "registration", M02: "registration", M03: "registration",
  M04: "registration", M05: "registration", M06: "registration",
  M07: "shipping", M08: "shipping", M09: "shipping",
  M10: "shipping", M11: "shipping", M12: "shipping",
  M13: "loan", M14: "loan", M15: "loan",
  M16: "loan", M17: "loan", M18: "loan",
});

export function resolveVariant(candidate) {
  return candidate && Object.hasOwn(MUTANT_TARGETS, candidate) ? candidate : "golden";
}

export function targetForVariant(variant) {
  return MUTANT_TARGETS[variant] ?? null;
}

async function loadModule(name, variant) {
  if (targetForVariant(variant) !== name) {
    return import(`./${name}.js`);
  }
  return import(`../mutants/${variant}/${name}.js`);
}

export async function loadVariantModules(variant) {
  const [registration, shipping, loan] = await Promise.all([
    loadModule("registration", variant),
    loadModule("shipping", variant),
    loadModule("loan", variant),
  ]);
  return { registration, shipping, loan };
}
