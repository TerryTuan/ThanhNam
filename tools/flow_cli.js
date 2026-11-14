// In ra JSON bản dịch tiếng Việt đã ghép liền mạch của một cuốn: node tools/flow_cli.js sach/<id>/du-lieu.json
const { flowOf } = require("./flow.js");
const book = JSON.parse(require("fs").readFileSync(process.argv[2], "utf8"));
process.stdout.write(JSON.stringify(flowOf(book.pages)));
