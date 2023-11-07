Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.


Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```
Assignment.py
----------------------
The file `assignment.py` consists in a first section where the function used in the program are defined, and a second one where they are exploited, in order to fulfill the task given in the assignment, namely to take all the golden boxes together.

The first function defined is the one named `drive`, which controls the robot to make him go straight with the desired speed, for the desired amount of time, in seconds.

The second function, `turn`, sets the input speed to the wheel, in a way that the robot turns on itself, for the desired time interval. This is made by setting to one wheel the velocity as it is, and to the other one the opposite value.

The function `find_token` finds the closest token which has a different code with respect to the list given as input, and returns its distance and angle with respect to the robot. It is used in the `main` function to look for the tokens not yet moved.

The `find_new_token` function looks for the list of tokens given as input, and returns its distance and angle.

The `reach_token` function manages to reach the closest token, ehich has a different code with respect to the ones in the input list. To do so, it exploits `find_token`. If the robot is not aligned with the token, it turn left or right, and then goes straight to reach it. When the robot is close enough to the target, namely it has a distance that is smaller that the threshold, 0.4, it grabs it with the method `R.grab()`.

The `explore` function provides to create a list of all the tokens seen in the arena. This is useful to decide when to stop looking for tokens.
First the robot drives straight, in order to get closer to the center of the arena. At this point it turns on itself once, and every time it sees a new token, it records it in a list, which will be returned at the end of the function.

The last function, `reach_goal`, provides to bring the grabbed token 



[sr-api]: https://studentrobotics.org/docs/programming/sr/
