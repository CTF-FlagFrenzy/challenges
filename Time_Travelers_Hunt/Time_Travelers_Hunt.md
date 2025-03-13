# Time_Travelers_Hunt

OSINT-Challenge where you have to get 3 flags. The challenge is split into three parts.

**Level**:Easy - Medium

## Challenge Overview:

In this challenge, we were tasked to find the flags using OSINT methods. 

---

### Part 1

The time traveler’s first clue is hidden in plain sight on their old blog. The blog was hosted at www.faketimemachine.rf.gd, but it has since vanished. Use your time machine (hint: archive.org) to recover their lost notes and find the first piece of the time capsule.

- Hint 1: Maybe you can find any kind archive in the internet?
- Hint 2: Your time machine is named archive.org ...
- Hint 3: Have a better look at the source.

### Part 2

Great work, traveler! You’ve found the first piece of the time capsule. But the next clue is more subtle. The second flag is hidden deeper within the echoes of the blog—inspect it carefully.

- Hint 1: Maybe you can find some images, that aren't that easy to access.
- Hint 2: Have a look at the hidden directories.
- Hint 3: dirbuster is a great tool.

### Part 3

You’re almost there! The third and final piece of the time capsule requires your problem-solving skills.

- Hint 1: There should be other files than images.
- Hint 2: Everyone knows Jack the Ripper.
- Hint 3: There are a lot of simple tools to find something.

## Technical guideline

### Website

The website can be pulled from repository via the CLI using the following command:
```
git pull https://github.com/CTF-FlagFrenzy/challenges.git
```
Under `challenges/Time_Travelers_Hunt/website/html/` is a file named congrats.html. 
First this website is deployed on a hosting platform with the name `www.faketimemachine.rf.gd`. Then this paged is saved at archive.org.

The `www.realtimemachine.rf.gd` is linked on the fake website. When looking at rest of the files e.g. `../img/` there are the different snippets from the QR-code. Those were sliced appart with Adobe Photoshop.

When looking at `../files/` a PDF file can be found. There is a password needed to unlock it and inside the flag is hidden.

**HAVE FUN**