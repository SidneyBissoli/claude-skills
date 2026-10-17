// Uso: node restore-libc.mjs <lock-antigo.json> <lock-novo.json>
// Devolve ao lock novo os blocos "libc" que o npm do Windows apaga,
// copiando-os do lock antigo pelo nome do pacote (libc não muda entre versões).
import { readFileSync, writeFileSync } from "node:fs";

const [oldPath, newPath] = process.argv.slice(2);
const oldLock = JSON.parse(readFileSync(oldPath, "utf8"));
const newText = readFileSync(newPath, "utf8");
const newLock = JSON.parse(newText);

if (JSON.stringify(newLock, null, 2) + "\n" !== newText.replace(/\r\n/g, "\n")) {
  console.error("ABORTA: o lock novo não faz ida e volta com JSON.stringify");
  process.exit(2);
}

// Guarda o libc e a chave que o precedia, para reinserir sem reordenar nada.
const libcByName = new Map();
for (const [k, v] of Object.entries(oldLock.packages)) {
  if (!v.libc) continue;
  const keys = Object.keys(v);
  libcByName.set(k.slice(k.lastIndexOf("node_modules/") + 13), {
    libc: v.libc,
    after: keys[keys.indexOf("libc") - 1],
  });
}

let restored = 0;
const semRef = [];
for (const [k, v] of Object.entries(newLock.packages)) {
  if (v.libc) continue;
  const name = k.slice(k.lastIndexOf("node_modules/") + 13);
  const ref = libcByName.get(name);
  if (!ref) {
    if (/linux.*(gnu|musl)|(gnu|musl).*linux/.test(name)) semRef.push(k);
    continue;
  }
  if (!(ref.after in v)) {
    console.error(`ABORTA: ${k} não tem a chave "${ref.after}" que precedia o libc`);
    process.exit(3);
  }
  const out = {};
  for (const [h, val] of Object.entries(v)) {
    out[h] = val;
    if (h === ref.after) out.libc = ref.libc;
  }
  newLock.packages[k] = out;
  restored++;
}

writeFileSync(newPath, JSON.stringify(newLock, null, 2) + "\n");
console.log(`libc devolvido: ${restored}`);
if (semRef.length) console.log(`SEM referência (conferir): ${semRef.join(", ")}`);
