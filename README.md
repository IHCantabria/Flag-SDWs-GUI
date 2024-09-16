# Flag-SDWs-GUI

This repository contains the GUI software developed to identify instances where a Satellite-Derived Waterline (SDW) is unable to accurately detect the land-water interface, whether partially or fully. The main objective is to label, within a preestablished options, which indicator the SDW is actually detecting. To do so, the present GUI facilitates the visualization of each SDW with its satellite image smoothly. Finally, the results are saved as a CSV file for further analysis.

## How to run the program?
**1. Install dependencies...**

  a) by creating new Anaconda environment:
  ``` bash
  conda env create --file environment.yml
  conda activate flag_sdw_gui
  ```
  b) directly from the requirements.txt file:
  ``` bash
  pip install -r requirements.txt
  ```
**2. Run the [main.py](https://github.com/IHCantabria/Flag-SDWs-GUI/tree/main/build/main.py) script located in the [build](https://github.com/IHCantabria/Flag-SDWs-GUI/tree/main/build) subfolder**
``` bash
python main.py
```

## Contact
For code-development issues contact 👨‍💻[Albert Gallego](gallegoa@unican.es).


</br>
</br>
<div align="center">
  <a href="https://github.com/AlbertGallegoJimenez/Flag-SDWs-GUI">
    <img src="images/Color_LogoAutoCos.png" alt="AutoCos logo" width="20%">
    </br>
    </br>
    <img src="images/01_Tira_resumen.png" alt="financing entities logos" width="75%">
  </a>
</div>
