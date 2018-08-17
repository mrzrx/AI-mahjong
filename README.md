AI-mahjong 
===

This is a smart mahjong implements by [joaming](https://github.com/joaming), [ghj](https://github.com/ghj227) and me on tensorflow.<br>
We mainly imitate AlphaGo zero's design ideas. The paper is here [Mastering the Game of Go without Human Knowledge](https://deepmind.com/documents/119/agz_unformatted_nature.pdf)<br>
<br>
***Thanks to our teacher Guo Wenhai very much!*** <br>
<br>
1. [Overview](#overview)<br>
2. [Play](#play)<br>
3. [Network](#network)<br>
4. [Result](#result)<br>
5. [Future](#future)<br>
6. [Reference](#reference)

## Overview

This is a two players' mahjong game.<br>
Every player makes an action across neural network's output(policy), and the datas produced on game will be updated by the result of game, then provided to neural network to training.

## Play

![](https://github.com/mrzrx/AI-mahjong/blob/master/image_for_readme/play.jpg)

## Network

![](https://charlesliuyx.github.io/2017/10/18/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BA%E7%9C%8B%E6%87%82AlphaGo%E5%85%83/ResNet.svg)
![](https://charlesliuyx.github.io/2017/10/18/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BA%E7%9C%8B%E6%87%82AlphaGo%E5%85%83/VPoutput.svg)

## Result  

![](https://github.com/mrzrx/AI-mahjong/blob/master/image_for_readme/result.jpg)

## Future

This project's result is not well. In fact, its intelligence looks like a baby, and the iteration time is too long. So there are many places to improve.

## Reference

[1] [深入浅出看懂AlphaGo元](https://charlesliuyx.github.io/2017/10/18/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BA%E7%9C%8B%E6%87%82AlphaGo%E5%85%83/#%E6%90%9C%E7%B4%A2%E7%AE%97%E6%B3%95)
