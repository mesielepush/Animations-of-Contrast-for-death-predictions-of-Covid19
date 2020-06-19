# Animations of contrasts for death prediction of Covid19
 This script and notebook produces mp4 animations, for contrasting real data of deaths for Covid19, with the predictions through time of [Youyang Gu](https://github.com/youyanggu/covid19_projections). It works for several countries.

 ![GIF EXAMPLE](test.gif)

Data come from [Youyang Gu repository](https://github.com/youyanggu/covid19_projections).

## Requeriments
* python 3.7
* pandas
* numpy
* matplotlib
* imageio
## Instructions
Download the repository.

You'll need the **'projections'** folder that's on the [Youyang Gu repository](https://github.com/youyanggu/covid19_projections).  

![repository](https://i.imgur.com/j7I7NZb.png)
 
Place it on the same folder as [prediction_animation.py](prediction_animation.py) and [Contrasts animations for Deaths predictions of Covid19.ipynb](https://github.com/mesielepush/Animations-of-Contrast-for-death-predictions-of-Covid19/blob/master/Contrasts%20animations%20for%20Deaths%20predictions%20%20of%20Covid19.ipynb):  

Then you can run it from the console by typing: ` python prediction_animation.py country_name ` replacling country_name with the name of the country to animate.

Otherwise you can open jupyter notebook and work on the [notebook](https://github.com/mesielepush/Animations-of-Contrast-for-death-predictions-of-Covid19/blob/master/Contrasts%20animations%20for%20Deaths%20predictions%20%20of%20Covid19.ipynb) so you'll be able to modify the plots.

### Warning:
I faced the next problem when running from the console:

**Error “could not find or load the Qt platform plugin windows”**

I solved it by following a response from [here](https://stackoverflow.com/questions/41994485/error-could-not-find-or-load-the-qt-platform-plugin-windows-while-using-matplo), by setting the `Library\plugins` Anaconda folder as `QT_PLUGIN_PATH` on the environment variables.

Running through Jupyter notebook has no problems.

Jonathan Marín - [Github](https://github.com/mesielepush)

</p>
<p align="center" style="display: flex; justify-content: center; align-items: center;">
    <a target="_blank" href="https://mail.google.com/mail/?view=cm&fs=1&tf=1&to=mesielepush@gmail.com">
      mesielepush@gmail.com
    </a> &nbsp; |
    <a target="_blank" href="https://github.com/mesielepush?tab=repositories">
       Portfolio
    </a> &nbsp; |
    <a target="_blank" href="https://www.linkedin.com/in/jonathan-nava-mar%C3%ADn-94659318b/">
      LinkedIn
    </a> &nbsp; |
    <a target="_blank" href="">
      Twitter
    </a>
</p>
