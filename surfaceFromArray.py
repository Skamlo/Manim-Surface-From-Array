from manim import *
import numpy as np


class SurfaceFromArray:
    def __init__(self):
        pass
    

    @staticmethod
    def __hashToRGB(hash:str):
        if hash[0] == '#':
            hash = hash[1:-1]

        rgb = []
        for i in (0, 2, 4):
            decimal = int(hash[i:i+2], 16)
            rgb.append(decimal)
        
        return list(rgb)


    @staticmethod
    def __RGBToHash(rgb:list):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


    def __setMinMax(self):
        self.min = self.array.min()
        self.max = self.array.max()


    def __colorFromHeight(self, dy, dx):
        xs = (self.array[dy, dx] - self.min) / (self.max - self.min)
        return self.gradientColor[int(xs * 100)]


    def __setGradientColor(self, color1:list, color2:list):
            def blendColor(c1, c2, blendIndex):
                return [
                    int(c1[0]*blendIndex + c2[0]*(1-blendIndex)),
                    int(c1[1]*blendIndex + c2[1]*(1-blendIndex)),
                    int(c1[2]*blendIndex + c2[2]*(1-blendIndex))
                ]

            for i in range(101):
                c3 = blendColor(color1, color2, (101 - i)/101)
                self.gradientColor.append(self.__RGBToHash(c3))


    def __checkArray(self):
        correct = True
        communicate = None

        # dtype
        if isinstance(self.array, np.ndarray):
            pass
        elif isinstance(self.array, list) or isinstance(self.array, tuple):
            self.array = np.array(self.array)
        else:
            correct = False
            communicate = "surfaceFromArray error: Incorrect array dtype. Only list, tuple or np.ndarray."

        # shape
        if correct:
            if not len(self.array.shape) == 2:
                correct = False
                communicate = "surfaceFromArray error: Incorrect array shape. Only two-dimensional array"

        if correct:
            if len(self.array) < 2 or len(self.array[0]) < 2:
                correct = False
                communicate = "surfaceFromArray error: Incorrect array shape. Minimum x and y axis is 2."

        if correct:
            if len(self.array) >= 100 and len(self.array[0] >= 100):
                communicate = "surfaceFromArray warning: x and y axis size is probably too big."
            elif len(self.array) >= 100:
                communicate = "surfaceFromArray warning: y axis size is probably too big."
            elif len(self.array[0] >= 100):
                communicate = "surfaceFromArray warning: x axis size is probably too big."

        return correct, communicate


    def __checkxLenght(self):
        correct = True
        communicate = None

        if not (
            isinstance(self.xLenght, float) or isinstance(self.xLenght, int) or
            isinstance(self.xLenght, np.float16) or isinstance(self.xLenght, np.float32) or isinstance(self.xLenght, np.float64) or
            isinstance(self.xLenght, np.float80) or isinstance(self.xLenght, np.float96) or isinstance(self.xLenght, np.float128) or
            isinstance(self.xLenght, np.float256)
        ):
            correct = False
            communicate = "surfaceFromArray error: Incorrect xLenght dtype. Only float or int."

        if correct:
            if self.xLenght <= 0:
                correct = False
                communicate = "surfaceFromArray error: Incorrect xLenght value. Only numbers greater than 0"

        if correct:
            if self.xLenght > 100:
                communicate = "surfaceFromArray warning: xLenght is probably too big"

        return correct, communicate
    

    def __checkyLenght(self):
        correct = True
        communicate = None

        if not (
            isinstance(self.yLenght, float) or isinstance(self.yLenght, int) or
            isinstance(self.yLenght, np.float16) or isinstance(self.yLenght, np.float32) or isinstance(self.yLenght, np.float64) or
            isinstance(self.yLenght, np.float80) or isinstance(self.yLenght, np.float96) or isinstance(self.yLenght, np.float128) or
            isinstance(self.yLenght, np.float256)
        ):
            correct = False
            communicate = "surfaceFromArray error: Incorrect yLenght dtype. Only float or int."

        if correct:
            if self.xLenght <= 0:
                correct = False
                communicate = "surfaceFromArray error: Incorrect yLenght value. Only numbers greater than 0"

        if correct:
            if self.xLenght > 100:
                communicate = "surfaceFromArray warning: yLenght is probably too big"

        return correct, communicate


    def __checkFillColor(self):
        self.isGradientColor = False
        self.gradientColor = []
        correct = True
        communicate = None

        def errorText():
            communicate = (
                "surfaceFromArray error: Incorrect fill_color value. " +
                "Only manim color object type or string hash color or " + 
                "list with two color - this case will generate a vertical gradien"
            )

        # case 1: [[255, 10, 10], [10, 10, 255]]
        # case 2: ['#ff0a0a', '#0a0aff']
        # case 3: [255, 10, 10]
        # case 4: '#ff0a0a'

        case = 0

        if isinstance(self.fill_color, list) or isinstance(self.fill_color, tuple) or isinstance(self.fill_color, np.ndarray):
            self.fill_color = np.array(self.fill_color)
            # case 1 check
            if len(self.fill_color.shape) == 2:
                if self.fill_color.shape[1] != 3:
                    correct = False
                    errorText()
                else:
                    error = False
                    for col in self.fill_color:
                        for value in col:
                            if value < 0 or value > 255:
                                error = True
                    if error:
                        correct = False
                        errorText()
                    else:
                        case = 1
            elif len(self.fill_color.shape) == 1:
                # case 2 check
                if isinstance(self.fill_color[0], str):
                    if self.fill_color.shape[0] == 2:
                        case = 2
                    else:
                        correct = False
                        errorText()
                # case 3 check
                elif isinstance(self.fill_color[0], int):
                    if self.fill_color.shape[0] != 3:
                        correct = False
                        errorText()
                    else:
                        error = False
                        for value in self.fill_color:
                            if value < 0 or value > 255:
                                error = True
                        if error:
                            correct = False
                            errorText()
                        else:
                            case = 3
                else:
                    correct = False
                    errorText()
        # case 4 check
        elif isinstance(self.fill_color, str):
            case = 4
        else:
            correct = False
            errorText()

        # converting fill_color
        if case == 1:
            self.isGradientColor = True
            self.__setGradientColor(
                self.fill_color[0],
                self.fill_color[1]
            )
        elif case == 2:
            self.isGradientColor = True
            self.__setGradientColor(
                self.__hashToRGB(self.fill_color[0]),
                self.__hashToRGB(self.fill_color[1])
            )
        elif case == 3:
            self.fill_color = self.__RGBToHash(self.fill_color)
        elif case == 4:
            pass

        return correct, communicate


    def __checkStrokeColor(self):
        correct = True
        communicate = None

        if isinstance(self.stroke_color, list) or isinstance(self.stroke_color, tuple) or isinstance(self.stroke_color, np.ndarray):
            self.stroke_color = np.array(self.stroke_color)
            if len(self.stroke_color.shape) != 1:
                correct = False
                communicate = "surfaceFromArray error: Incorrect stroke_color value. Incorrect array shape - only 1D array."
            else:
                if len(self.stroke_color) != 3:
                    correct = False
                    communicate = "surfaceFromArray error: Incorrect stroke_color value. Incorrect number of color channels. Only three RGB channels."
                else:
                    if self.stroke_color[0] < 0 or self.stroke_color > 255:
                        correct = False
                        communicate = "surfaceFromArray error: Incorrect stroke_color value. Red value out of correct interval. Only values in [0, 255] interval."
                    elif self.stroke_color[0] < 0 or self.stroke_color > 255:
                        correct = False
                        communicate = "surfaceFromArray error: Incorrect stroke_color value. Green value out of correct interval. Only values in [0, 255] interval."
                    elif self.stroke_color[0] < 0 or self.stroke_color > 255:
                        correct = False
                        communicate = "surfaceFromArray error: Incorrect stroke_color value. Blue value out of correct interval. Only values in [0, 255] interval."
            if correct:
                self.stroke_color = self.__RGBToHash(self.stroke_color)
        elif isinstance(self.stroke_color, str):
            pass
        else:
            correct = False
            communicate = "surfaceFromArray error: Incorrect stroke_color value. Only string with hash color or list with RGB values."

        return correct, communicate
            

    def __checkFillOpacity(self):
        correct = True
        communicate = None
        
        if self.fill_opacity < 0 or self.fill_opacity > 1:
            correct = False
            communicate = "surfaceFromArray error: Incorrect fill_opacity value. Only between 0 and 1."

        return correct, communicate


    def __checkStrokeOpacity(self):
        correct = True
        communicate = None
        
        if self.stroke_opacity < 0 or self.stroke_opacity > 1:
            correct = False
            communicate = "surfaceFromArray error: Incorrect stroke_opacity value. Only between 0 and 1."

        return correct, communicate


    def generate(
            self, array:np.ndarray, xLenght:float = 6, yLenght:float = 6,
            fill_color='#ffff00', fill_opacity:float=0.5,
            stroke_color='#ffffff', stroke_opacity:float=0
        ):
        '''
        `array`: 2D array contains height map. Only np.ndarray, list or tuple. Minimum x and y size is 2.

        `xLenght`: Lenght of surface on x axis. Only float or int values. Greater than 0.

        `yLenght`: Lenght of surface on y axis. Only float or int values. Greater than 0.

        `fill_color`: Color of surface polygons. Only manim color object type or string hash color or list with two color - this case will generate a vertical gradient.

        `fill_opacity`: Opacity of surface polygons. Only float value in [0, 1] interval.

        `stroke_color`: Color of surface polygons edges. Only manim color object type or string hash color.

        `stroke_opaicty`: Opacity of surface polygons edges. Only float value in [0, 1] interval.
        '''

        self.array = array
        self.xLenght = xLenght
        self.yLenght = yLenght
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.stroke_color = stroke_color
        self.stroke_opacity = stroke_opacity

        correct = True
        communicate = None

        def showCommunicate():
            print(communicate)
            communicate = None

        if correct:
            correct, communicate = self.__checkArray()
        if (not correct) and (communicate != None):
            showCommunicate()

        if correct:
            correct, communicate = self.__checkxLenght()
        if (not correct) and (communicate != None):
            showCommunicate()

        if correct:
            correct, communicate = self.__checkyLenght()
        if (not correct) and (communicate != None):
            showCommunicate()

        if correct:
            correct, communicate = self.__checkFillColor()
        if (not correct) and (communicate != None):
            showCommunicate()
            
        if correct:
            correct, communicate = self.__checkStrokeColor()
        if (not correct) and (communicate != None):
            showCommunicate()
        
        if correct:
            correct, communicate = self.__checkFillOpacity()
        if (not correct) and (communicate != None):
            showCommunicate()

        if correct:
            correct, communicate = self.__checkStrokeOpacity()
        if (not correct) and (communicate != None):
            showCommunicate()

        self.__setMinMax()

        if correct:
            map = np.array(
                [
                    [
                        [x, y]
                        for x in np.linspace(-xLenght/2, xLenght/2, len(array[0]))
                    ]
                    for y in np.linspace(-yLenght/2, yLenght/2, len(array))
                ]
            )

            polygons = VGroup()

            for dy in range(len(self.array)-1):
                for dx in range(len(self.array[0])-1):
                    if self.isGradientColor:
                        self.fill_color = self.__colorFromHeight(dy, dx)

                    polygon1 = Polygon(
                        *[
                            [map[dy, dx, 0], map[dy, dx, 1], array[dy, dx]],
                            [map[dy, dx+1, 0], map[dy, dx+1, 1], array[dy, dx+1]],
                            [map[dy+1, dx+1, 0], map[dy+1, dx+1, 1], array[dy+1, dx+1]]
                        ],
                        stroke_opacity=self.stroke_opacity,
                        stroke_color=self.stroke_color,
                        fill_opacity=self.fill_opacity,
                        fill_color=self.fill_color
                    )

                    polygon2 = Polygon(
                        *[
                            [map[dy, dx, 0], map[dy, dx, 1], array[dy, dx]],
                            [map[dy+1, dx, 0], map[dy+1, dx, 1], array[dy+1, dx]],
                            [map[dy+1, dx+1, 0], map[dy+1, dx+1, 1], array[dy+1, dx+1]]
                        ],
                        stroke_opacity=self.stroke_opacity,
                        stroke_color=self.stroke_color,
                        fill_opacity=self.fill_opacity,
                        fill_color=self.fill_color
                    )

                    polygons.add(polygon1)
                    polygons.add(polygon2)

            return polygons
    