# Metamers
This repository contains Python code on the topic of metamer mismatching, in particular a re-implementation of the algorithm described in [1].

At the beginning of my research, almost all legacy code was only available in Matlab.
My original motivation was to create a unified Python framework.
Due to the lack of time, the project was abandoned after I left research.
Due to various requests for the implementation of [1] and talks with fellow researchers, I decided to refactor and finally publish relevant parts of the codebase.
A visual tutorial on the concept of metamer mismatching is also included.

If you find it useful or use it in your own research, kindly cite the associated publications [1, 2].

## About Me
My name is Tarek Luttermann (formerly Tarek Stiebel).
I received my Dr.-Ing (Ph.D) in electrical engineering from RWTH Aachen University in 2021.
During my time as a research scientist at the Institute of Imaging and Computer Vision, i was responsible for the field of multi-spectral imaging.
This mainly covered various applications and projects in industry.
However, I also found interest in color science and, in particular, metamerism.

Feel free to connect with me on LinkedIn if you want to discuss these topics.

##  Background
Two objects are said to be *metameric*, if they lead to identical color signals although having different object reflectances.
The "metamer set" is the set of all theoretically possible object reflectances that lead to a given color signal.
The "metamer mismatch volume" describes the metamer set observed under different viewing conditions, for example under a different illumination or by a different observer.
The change in viewing condition will most likely cause the original metamer set to project to an entire volume of color signals, the metamer mismatch volume or metamer mismatch body.
Assuming that spectral object reflectances must be within the range [0, 1], Logvinenko [3] proposed a set a functions that describe the theoretical bounds of metamer mismatch bodies in terms of optimal reflectance functions.

*Optimal colors* that are associated with *optimal reflectance functions* were first postulated by Willhelm Ostwald at the beginning of the 20th century.
Erwin Schrödinger proved in 1919 that optimal colors in fact bound the set of all colors theoretically observable to the human observer.
The concept of optimal colors has been fundamental for various researchers throughout the 20th century.
Optimal colors and associated optimal reflectance functions are likewise fundamental to the theory on metamer mismatching by Logvinenko.

### Related Work
The theory developed by Logivenko [3] can be interpreted in different ways.
Multiple publications have since been published.
Next to the more theoretical approach by Logvinenko, there have also been approaches motivated by real-world observations.
For example, the data driven approach by Finlayson [7] most certainly deserves special mention.
Here is a short list of publications, mostly related to the theory by Logvinenko, that you might find interesting in context of this repository.
* [1] A Robust Algorithm for Computing Boundary Points of the Metamer Mismatch Body, *Tarek Stiebel and Dorit Merhof*, In: Twenty-sixth Color and Imaging Conference (CIC), 2018
* [2] The Importance of Smoothness Constraints on Spectral Object Reflectances when Modeling Metamer Mismatching, *Tarek Stiebel and Dorit Merhof*, In: IEEE International Conference on Computer Vision Workshop (ICCVW), 2017
* [3] Metamer Mismatching, *Alexander D. Logvinenko and Brian V. Funt and Christoph Godau*, IEEE Transactions on Image Processing, 23, 34-43, 2014
* [4] A Simple Algorithm for Metamer Mismatch Bodies, *Paul Centore*, 2017
* [5] Spherical sampling methods for the calculation of metamer mismatch volumes, *Michal Mackiewicz, Hans Jakob Rivertz, Graham D. Finlayson*,  J. Opt. Soc. Am. A 36, 96-104, 2019
* [6] Metamer mismatching in practice versus theory, *Xiandou Zhang, Brian Funt, and Hamidreza Mirzaei*, J. Opt. Soc. Am. A 33, A238-A247, 2016
* [7] Metamer Sets, *Graham D. Finlayson and Peter Morovic*, J. Opt. Soc. Am. A 22, 810-819 (2005)
* [8] Metamer Mismatching and Its Consequences for Predicting How Colours are Affected by the Illuminant, *X. Zhang, B. Funt and H. Mirzae*, IEEE International Conference on Computer Vision Workshop (ICCVW), 2015

I do by no means claim above list to be a complete representation of the field.
If there is other work you would like to see incorporated, kindly contact me.

# Visualizing Underlying Geometric Concepts
Here is a brief tutorial on the theory of metamer mismatching by Logvinenko as well as the geometric interpretation.

Let us consider the following scenario:
There is one human observer located indoors (1964 standard observer under CIE A) and one human observer located outdoors (1964 standard observer under CIE D65).
It is an example to showcase the concept of illuminant induced metamer mismatching.
The color matching functions of the human observer as well as the spectral power distributions of the illuminants are shown below.
<p align="center">
    <img src="data/figures/cmfandspd.png" />
</p>

The spectral power distribution of the light can be combined with the color matching functions to form spectral weights.
The spectral weights associated with both viewing conditions are visualized in the following plots.
<p align="center">
    <img src="data/figures/spectral_weights.png" />
</p>
Spectral weights allow us to compute color signals when viewing an object. 
The object is hereby given by its spectral object reflectance $`r(\lambda)`$. 

$`\int \sigma(lambda) r(\lambda)`$
