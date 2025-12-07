import { readFileSync, writeFileSync } from 'node:fs'

if (!process.argv[2]) throw new Error('Please provide version')
const version = process.argv[2].slice(1)

const setVersion = (path) =>
    writeFileSync(path, readFileSync(path, 'utf8').replace('0.0.0', version))

setVersion('./package.json')
setVersion('./src/index.ts')
