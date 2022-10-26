<h1>🎞Python script "VideoCutter"🎞</h1>
<h4>*👨🏻‍💻 It was an order</h4>
<h2>📄The description of the work: </h2>
<p>
Initially, I had the task of creating a script that would collect data when launched. As input we get:
<ul>
<li>interval of desired video's length</li>
<li>videos quality</li>
<li>number of required folders</li>
<li>number of processor threads</li>
<li>path to the folder with videos</li>
<li>path to the folder with music</li>
</ul>
</p>
<h3>🧩The essence of the work:</h3>
<p>We receive an unlimited number of videos for input. The purpose of the script is to:
<ul>
<li>create a main folder in the directory where the script is located</li>
<li>create folders whose name consists of the number of videos in them (For example, 1-15, 16-30, 31-38)</li>
<li>collect one video from the original videos in a user-defined interval, adjusting the video quality</li>
<li>delete the old audio track of the builded video and add new music, which we first take from the music folder and mix randomly</li>
<li>all videos are created strictly in the specified interval. If the original video is larger than the maximum spacing, then it will be cut off</li>
</ul>
</p>
<p>Video rendering involves the same number of threads that we use in the source data.</p>
<p>There should be 14 such "medium rare" videos in a folder, and the 15th video should be a splicing of the previous 14.</p>
<p>The 15th video is merged only after all folders have been created, and "middle videos" have been created in them.</p>

<h2>🗂Conclusion:</h2>
<p>The script does its job very well. Automatic work is always more pleasant than manual work.</p>
<p>All user errors will be caught, there are hints on what to enter where, and annotations and docstrings are written for developers.</p>
<h3>❗Attention❗</h3>
<p>A script-killing error [WinError 6] may be thrown during script execution.</p>
<p>This is due to the peculiarities of the descriptor of the Windows operating system. On Linux OS, this error should not be. </p>
<p>I came across this on certain videos, I don’t know if they can be “broken”, but when I deleted them and ran the script again, everything worked out fine.</p>
<p>If you know how to solve this problem, then you can help me by creating a pull request with your solution.</p>
