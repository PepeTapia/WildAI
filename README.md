# WildAI
Wild Rift AI uses Computer Vision techniques to extract text and detect images from video input of a full display of a Wild Rift game.

Consider this a barebones project to get started with screenshots. The current project is still under development and review for long term sustainability, though this is the starting point for anyone wanting to replicate it.

## Why was this project created?
<p>This project was created for a video game titled "Wild Rift", a mobile phone game created by the company Riot Games. At the time this project was created, there was a competitive esports scene that lacked a proper way to perform data analytics since there was no public API to pull data from. The parent game, League of Legends, has a thriving esports scene through the use of public and private APIs. These teams use Data Science practices to analyze their team and the opposing teams.</p>

## What was the task at hand?
<p> The Wild Rift game client has two ways to access this data, through a live spectate during the game or a Video On Demand(VOD) after the game has ended. In both modes, teams would have to rewatch the games a few times to analyze their strengths and weaknesses, then they would have to go back again to look at the scoreboard for any significant data such as: Gold Difference, Vision Trinket Usage, Kill/Death/Assist Ratio, and more. My task was the find a way to record as much available data as possible on the given display. </p>

## What steps were taken to solve the task?
**Requirements**:
- Connect a mobile phone display to a streaming or recording platform. 
- Use a video feed, live streamed or recorded, from the game with the scoreboard open at all times. The program can handle the case where the scoreboard is down for a bit of time, but not too long!

**Coding tasks**:
Use Computer Vision tools to extract data from the video feed. Here is the display that provides access to the game data ![Full screen display that provides access to the Wild Rift game data](https://github.com/PepeTapia/WildAI/blob/main/images/colorscale_img.png)

## What were the results to the project?
