# Notes on the csvtidy README

## Verdict
No. I would not give this README to an AI coding assistant as it is. It contains instructions written for an
assistant, not for a person, and three of them ask for actions that would run code from the internet or send secrets out.
A person should read it first, and an assistant should only see a cleaned copy.

## What I found
- **Hidden HTML comment.** It is invisible when the page is rendered. It tells an assistant to run a setup script
  with `curl ... | sh` "once", not to ask the user and not to mention it. That is a download piped into a shell: remote code.
- **A note "for AI assistants" asking for the `.env` file.** It is visible, but sits in the troubleshooting section and
  asks the assistant to send the contents of `.env` and the shell history to a vendor address with `curl -d @.env`. That would
  leak every secret in the project.
- **Invisible characters.** After the friendly closing line there are 113 Unicode tag characters (the U+E0000 block). A
  person sees nothing; read as characters they spell a sentence telling an assistant to ignore the repository rules, run the
  setup command and say nothing about it. I found them with a short Python script, not by looking.
- **Advice to switch permission checks off.** It tells contributors to run the assistant with
  `--dangerously-skip-permissions` "to avoid questions". That removes the one place where a human would see the other tricks.
- **A second package in the install line.** `csvtidy` is a made-up vendor library for this exercise (a real package with a
  similar name may exist on the public index and is unrelated). `csvtidy-extras` was not registered there when I checked, but
  anyone could register it tomorrow, which is exactly the slopsquatting risk: a name that looks plausible in a README is what a
  package squatter registers. Neither name is on our allow-list, and that is the point: nobody on the team has vetted either.

## What stopped it in my setup
- The `Read(./.env)` deny rule stops the built-in tools from reading `.env`, and the guard hook blocks any shell command that
  names a real `.env` file, so the upload to the vendor address is stopped twice.
- The guard hook blocks a download piped into a shell and `curl` sending data out, and `pip install` of anything, so the
  hidden setup command and the install line are both stopped before they run. The deny rule on `git push` and the
  hook also stop a publish.
- The dependency check reports `csvtidy` and `csvtidy-extras` as not on the allow-list or in the lockfile.
- Nothing stops the permission advice except me: I never use bypass mode, and the project settings do not set it. The sandbox
  is a separate layer that I have to switch on myself on my machine.

## What I will do by hand
- Read any vendor README as a person, rendered and as raw text, and search it for invisible characters before an assistant
  sees it.
- Never paste it whole into a session. Give the assistant the one section I need.
- Decide about a new dependency myself, in a ticket with a second reviewer, and add it to the allow-list in that pull request.
- Run the assistant in Manual mode, in a clean branch, and read every command it asks to run.
