# Build Your Own LOC Counter
This challenge is to build your own version of the tools cloc, sloc and scc. These tools count lines of code and produce statistic on the number of lines in the source code, the lines of code, the lines of comments, the empty lines and so on.

Some also calculate the COCOMO 81 and COCOMO II estimates for the software being analysed. If you’re not familiar with it, the COCOMO model was developed by Barry W. Boehm to estimate the effort, cost and schedule for software projects. I wouldn’t rely on these numbers to plan a software project, but they’re an interesting tool to compare existing projects and get a feel for the size and scope of them.

Counting the lines of code in a software project sounds trivial and quite honestly seems like something you could do in a short bash command, i.e.:

`% find . -name '*.go' | xargs wc -l | sort -nr`

However if you want to do it accurately and fast, you can get into some interesting computer science challenges. And when it comes to scc, I mean blazingly fast!

# But Why Count Lines Of Code?

TL/DR: It’s useful as a gauge of the size and complexity of a project, but if you want much more detail Ben Boyter, the author of scc wrote a blog post explaining why he put so much effort into building a tool to count lines of code.