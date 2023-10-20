const {danger, warn, fail} = require('danger')

const title = danger.github.pr.title.trim()
const body = danger.github.pr.body.trim()
const isUser = danger.github.pr.user.type === "User"

if (isUser) {
  if (body.includes("Summarize the added feature or bug fix")) {
    fail(`Please include meaningful description.`);
  }

  if (body.includes("Elaborate on things that the reviewer")) {
    fail(`Please include meaningful description.`);
  }
}
