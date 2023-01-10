<h1> 2023-Jetson-Code </h1>
<p>
	A repository that contains code to will run on FRC 2199's Nvidia Jetson coprocessor during the 2023 season.
</p>

</br>

<h2> Setting Up the Jetson </h2>
<p>
	Please see the instructions <a href="https://github.com/PIE-Cubed/2023-Jetson-Code/wiki/Setup#----setting-up-the-jetson-nano">here</a> for setting up a Nvidia Jetson.
</p>

</br>

<h2> Prerequisites </h2>
<p>
	<ul>
		<li>A <a href="https://www.python.org/downloads/">Python 3</a> environment (prefereably <a href="https://www.python.org/downloads/release/python-3108/">3.10.8</a>)</li>
		<li>The <a href="https://pypi.org/project/opencv-contrib-python/">OpenCV Contributor</a> package</li>
		<li>The <a href="https://pypi.org/project/numpy/">NumPy</a> package (should install with OpenCV)</li>
		<li>The <a href="https://pypi.org/project/robotpy/">RobotPy</a> package</li>
		<li>The <a href="https://pypi.org/project/transforms3d/">Transforms3d</a> package</li>
		<li>The <a href="https://pypi.org/project/pupil-apriltags/">Pupil Apriltags</a> package</li>
	</ul>
</p>

</br>

<h2> Installation </h2>
<h3> If on Linux: </h3>
<p>
	Download <a href="https://github.com/PIE-Cubed/2023-Jetson-Code/blob/main/Install.sh">Install.sh</a> and run it from the terminal using this command: 
	
	sh Install.sh
</p>
<p>
	<strong>Note: DO NOT run the above command with root provledges as that will cause cmake and pip to install their packages to the wrong location, breaking other package dependencies.</strong>
</p>
</br>
<h3>If on Windows:</h3>
<p>
	<ul>
		<li>Follow the instructions at the Python 3 link to install Python 3 for Windows.</li>
		<li>Install the above packages using their respective pip commands.</li>
	</ul>
</p>

</br>

<h2> Writing Programs for Jetson </h2>
<p>
	This is addressed in detail <a href="https://github.com/PIE-Cubed/2023-Jetson-Code/wiki">here</a>, in the repository's wiki.
</p>

</br>

<h2> More details </h2>
<p>
	If you'd like to learn more, all of these sections (and more!) will be explained in greater detail in the repository's <a href="https://github.com/PIE-Cubed/2023-Jetson-Code/wiki">wiki</a>.
</p>