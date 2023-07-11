import colorsys
import numpy as np
import matplotlib.pyplot as plt


class Colornal:
    def __init__(self,h=None,l=None,s=None) -> None:
        self.h = h
        self.l = l
        self.s = s
        self.__N = 0


    def __check_N(self) -> None:
        if len(self.h) == len(self.l) == len(self.s):
            self.__N = len(self.h)
        else:
            raise IndexError("The length of h, l, s must be equal.")
        

    def __check_value(self) -> None:
        temp_array = np.concatenate((self.h,self.l,self.s))
        min_value = np.min(temp_array)
        max_value = np.max(temp_array)
        if min_value < 0 or max_value > 1:
            raise ValueError("The value of h, l, s must be between 0 and 1.")
    
    
    def draw(self) -> None:
        self.__check_N()
        self.__check_value()

        rgb_array = np.vstack((self.h,self.l,self.s)).T
        # Transform HLS to RGB
        for i in range(self.__N):
            rgb_array[i] = list(colorsys.hls_to_rgb(rgb_array[i][0], rgb_array[i][1], rgb_array[i][2]))

        # Draw
        x = np.linspace(0, 1, self.__N)
        fig, axs = plt.subplots(4,1,figsize=(5,8))
        # ax0,1,2,3 for Hue, Lightness, Saturation, Colorband
        axs[0].plot(x, self.h, color='black')
        axs[0].set_title('Hue')
        axs[0].set_ylim(0,1.1)
        axs[1].plot(x, self.l, color='black')
        axs[1].set_title('Lightness')
        axs[1].set_ylim(0,1.1)
        axs[2].plot(x, self.s, color='black')
        axs[2].set_title('Saturation')
        axs[2].set_ylim(0,1.1)
        axs[3].imshow(rgb_array.reshape(1,-1,3), aspect='auto')
        axs[3].axis('off')

        fig.subplots_adjust(top=0.85, hspace=0.8)
        plt.show()


if __name__ == "__main__":
    N = 500
    x = np.linspace(0, 1, N)

    h = 0.5*np.sin(np.pi/4*x+np.pi) + 0.5
    l = 0.5*np.sin(np.pi/2*x) + 0.5
    s = 0.5*np.ones(N)
    cs = Colornal(h,l,s)
    cs.draw()