import { copyFileSync } from 'node:fs'

copyFileSync('../build/dist/engine/EngineConfiguration', '../dist/EngineConfiguration')
copyFileSync('../build/dist/engine/EnginePlayData', '../dist/EnginePlayData')
copyFileSync('../build/dist/engine/EngineWatchData', '../dist/EngineWatchData')
copyFileSync('../build/dist/engine/EnginePreviewData', '../dist/EnginePreviewData')
copyFileSync('../build/dist/engine/EngineTutorialData', '../dist/EngineTutorialData')
copyFileSync('../build/dist/engine/EngineRom', '../dist/EngineRom')
copyFileSync('./res/thumbnail.png', '../dist/thumbnail.png')
