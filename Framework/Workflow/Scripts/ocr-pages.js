#!/usr/bin/env node
"use strict";

// OCR PNG pages with tesseract.js from PHIL_OCR_HOME.
//
// One worker is reused for every image. Language data is read only from the
// local --tessdata directory, with caching disabled, so recognition never
// touches the network. Output is one JSON object per image on stdout.

const fs = require("fs");
const os = require("os");
const path = require("path");

function usage() {
    return (
        "usage: node ocr-pages.js --lang eng --tessdata <dir> " +
        "<png> [<png> ...]"
    );
}

function parseArgs(argv) {
    const options = { lang: "eng", tessdata: null, images: [] };
    for (let index = 0; index < argv.length; index += 1) {
        const arg = argv[index];
        if (arg === "--lang") {
            options.lang = argv[index + 1];
            index += 1;
        } else if (arg === "--tessdata") {
            options.tessdata = argv[index + 1];
            index += 1;
        } else if (arg === "--help" || arg === "-h") {
            process.stdout.write(usage() + "\n");
            process.exit(0);
        } else if (arg.startsWith("--")) {
            throw new Error(`unknown option: ${arg}`);
        } else {
            options.images.push(arg);
        }
    }
    if (!options.lang) {
        throw new Error("--lang must not be empty");
    }
    if (!options.tessdata) {
        throw new Error("--tessdata is required");
    }
    if (!options.images.length) {
        throw new Error("at least one PNG is required");
    }
    return options;
}

function runtimeHome() {
    if (process.env.PHIL_OCR_HOME) {
        return process.env.PHIL_OCR_HOME;
    }
    if (process.env.LOCALAPPDATA) {
        return path.join(process.env.LOCALAPPDATA, "phil-ocr");
    }
    return path.join(os.homedir(), ".phil-ocr");
}

function loadTesseract(home) {
    const modulePath = path.join(home, "node_modules", "tesseract.js");
    if (!fs.existsSync(modulePath)) {
        throw new Error(
            `tesseract.js is not installed in ${home}; run pdf-extract.py ocr-setup`
        );
    }
    return require(modulePath);
}

// tesseract.js exposes line boxes either at the top level or inside
// blocks -> paragraphs -> lines, depending on the version.
function collectLines(data) {
    if (Array.isArray(data.lines) && data.lines.length) {
        return data.lines;
    }
    const lines = [];
    for (const block of data.blocks || []) {
        if (Array.isArray(block.lines)) {
            lines.push(...block.lines);
        }
        for (const paragraph of block.paragraphs || []) {
            if (Array.isArray(paragraph.lines)) {
                lines.push(...paragraph.lines);
            }
        }
    }
    return lines;
}

function normalizeLine(line) {
    const bbox = line.bbox || {};
    return {
        text: typeof line.text === "string" ? line.text : "",
        bbox: [bbox.x0, bbox.y0, bbox.x1, bbox.y1],
        confidence:
            typeof line.confidence === "number" ? line.confidence : 0,
    };
}

async function main() {
    const options = parseArgs(process.argv.slice(2));
    const home = runtimeHome();
    const tesseract = loadTesseract(home);
    const worker = await tesseract.createWorker(options.lang, 1, {
        langPath: options.tessdata,
        cacheMethod: "none",
        gzip: false,
        logger: () => {},
    });
    try {
        for (const image of options.images) {
            // v7 returns text and confidence by default; block boxes are
            // loaded only when the output option asks for them.
            const { data } = await worker.recognize(image, {}, { blocks: true });
            const payload = {
                png: path.resolve(image),
                confidence:
                    typeof data.confidence === "number"
                        ? data.confidence
                        : 0,
                text: typeof data.text === "string" ? data.text : "",
                lines: collectLines(data).map(normalizeLine),
            };
            process.stdout.write(JSON.stringify(payload) + "\n");
        }
    } finally {
        await worker.terminate();
    }
}

main().catch((error) => {
    const message =
        error && error.message ? error.message : String(error);
    process.stderr.write(`ocr-pages.js: ${message}\n`);
    process.exit(1);
});
