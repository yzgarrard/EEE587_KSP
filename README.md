# Kerbal Space Program - complex environment for Reinforcement Learning

Below you can find medium article with whole story and short tutorial how to start.

[https://medium.com/@whiteastercom/kerbal-space-program-complex-environment-for-reinforcement-learning](https://medium.com/@whiteastercom/kerbal-space-program-complex-environment-for-reinforcement-learning-12318db065f5)

#

### Files description:

[log](https://github.com/under-control/flytosky/tree/master/log) - tensorflow session with results csv

[a3c_continous.py](https://github.com/under-control/flytosky/blob/master/a3c_continous.py) - a3c network with workers

[config.py](https://github.com/under-control/flytosky/blob/master/config.py) - setting parameters and connections

[ksp_env.py](https://github.com/under-control/flytosky/blob/master/ksp_env.py) - game environment

[requirements.txt](https://github.com/under-control/flytosky/blob/master/requirements.txt) - Python 3.6

[results_plotter.py](https://github.com/under-control/flytosky/blob/master/results_plotter.py) - plotter updated continuously

[tracker.py](https://github.com/under-control/flytosky/blob/master/tracker.py) - shows the data in console and inside the game

#
Piotr Kubica - Machine Learning Engineer at [Whiteaster](https://whiteaster.com/)

### How to run

Original tutorial from [https://medium.com/@whiteastercom/kerbal-space-program-complex-environment-for-reinforcement-learning](https://medium.com/@whiteastercom/kerbal-space-program-complex-environment-for-reinforcement-learning-12318db065f5)

Install the game Kerbal Space Program (no extensions needed)

Download https://github.com/krpc/krpc/releases/download/v0.4.8/krpc-0.4.8.zip

Unpack zip, open it go to GameData and copy only folder kRPC to GameData directory where you’ve installed the game, it will propably be:
Kerbal Space Program/game/GameData

Download: https://krpc.github.io/krpc/_downloads/51d10d60684108532ec1a5b93393faab/LaunchIntoOrbit.craft and put this file to:
Kerbal Space Program/game/Ships/VAB

Download the save “kill” [https://drive.google.com/file/d/1L1DdeUdHpcMSmO8royVWocitVR93UwdE], unpack it and paste whole folder to:
Kerbal Space Program/game/saves
(if this save will not work, just create Sandbox game named “kill” go to Launchpad with LanuchIntoOrbit ship and save game with name “revivekerbals” when on the Lanuchpad)

Run the game -> Start game -> Resume Game ->
Select “kill” save -> Load -> Click on the Launchpad
-> click twice on Launch Into Orbit (Stock)-> “Launchpad not clear message” appears — select -> Go to LaunchIntoOrbit on Launchpad->

You should see now the rocket on Launchpad and kRPC add on.
-> click “Add server” -> then click “Start server”

You should either allow connection for certain ip or auto-accept new clients in advanced server settings.

Clone the repository:
https://github.com/under-control/flytosky

If you got connection you can start a3c_continous.py

If you want to run more agents you can add new servers. Remember to change RPC and stream ports in order to differentiate workers.

If you want to connect to other computers in your local network via IP,
click Edit and change Address: from “localhost” to “Any”.

If you want to modify the states, controls, or rewards, look into ksp_env.py.

Lowering graphics as below is also a good idea to improve performance.
