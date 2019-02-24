Files used for the case study from *Efficient attack-defense trees analysis using Pareto attribute domains*.
* [*reconfigure_power_meter.xml*](./reconfigure_power_meter.xml) - .xml file storing the case study tree. Can be provided as input to [ADTool](https://satoss.uni.lu/members/piotr/adtool/) for graphical visualization.
* [*consensus.txt*](./consensus.txt) - the basic assignment of attributes to the basic actions of the opponent.
* [*study.py*](./study.py) - Python script used for performing the case study.

The following steps lead to reproducing the results.

1. Install Python, version >= 3.5.6.
2. Install the [adtrees](https://github.com/wwidel/adtrees) package using `pip install adtrees`.
3. Download the contents of this repository.
4. In the folder where the contents of this repository are stored, run `python study.py`. See comments in the code.
