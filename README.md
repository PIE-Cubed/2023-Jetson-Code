<h1> 2023-Jetson-Code </h1>
<p>
	A repository that contains code to will run on FRC 2199's Nvidia Jetson coprocessor during the 2023 season.
</p>

<h2> Setting Up the Jetson </h2>
<p>
	Not yet completed...
</p>

<h2> Prerequisites </h2>
<p>
	<ul>
		<li>A <a href="https://www.python.org/downloads/">Python 3</a> environment (prefereably <a href="https://www.python.org/downloads/release/python-3108/">3.10.8</a>)</li>
		<li>The <a href="https://pypi.org/project/opencv-contrib-python/">OpenCV Contributor</a> module</li>
		<li>The <a href="https://pypi.org/project/numpy/">NumPy</a> module (should install with OpenCV)</li>
		<li>The <a href="https://pypi.org/project/robotpy/">RobotPy</a> module</li>
		<li>The <a href="https://pypi.org/project/transforms3d/">Transforms3d</a> module</li>
		<li>The <a href="https://github.com/AprilRobotics/apriltag">Official AprilTags</a> module</li>
		<li>The <a href="https://pypi.org/project/dt-apriltags/">Duckie Town Apriltags</a> module</li>
	</ul>
</p>

<h2> Installation of Prerequisites </h2>
<p>
	If on Linux, download InstallPrerequisites.sh.
	Once downloaded, open a terminal and tun this command:
	
	$ sh InstallPrerequisites.sh
</p>
<p>
	AFTER running the script, it will prompt you for a root password. DO NOT enter the root password BEFORE running the above command as it breaks a lot of the module dependencies.
</p>
<p>
	&nbsp
</p>
<p>
	If not on Linux:
	<ul>
		<li>Follow the instructions at the Python 3 link to install Python 3 for your operating system.</li>
		<li>Install OpenCV Contributor, RobotPy, and Transforms3d with their respective pip commands.</li>
	</ul>
	<strong>Please Note: The AprilTag detector we use is Linux exclusive and WILL NOT run on any other OS.</strong>
</p>

<h2> Writing Programs for Jetson </h2>
<p>
	Not yet completed...
</p>