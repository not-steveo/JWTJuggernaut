<b>JWTJuggernaut</b>

A work in progress.

I hope to create a tool that can serve as a Swiss Army Knife for testing JWT implementations, with a focus on automating attacks and being highly configurable. I primarily use [Ticarpi's jwt_tool](https://github.com/ticarpi/jwt_tool/tree/master) and Burp Suite's [JWT Editor plugin](https://portswigger.net/bappstore/26aaa5ded2f74beea19e2ed8345a93dd) when testing JWTs, and with this tool I hope to combine features from both into a single do-it-all tool. A main feature that I plan to implement that I would find useful in my own testing is the ability to pass the tool an HTTP request in a txt file, which is easily one of my favorite features of SQLMap. My initial goals for this tool are to implement functionality to solve all of the (BurpSuite Practitioner JWT labs)[https://portswigger.net/web-security/jwt] with as little user interaction as possible, automating attack steps wherever I can.
