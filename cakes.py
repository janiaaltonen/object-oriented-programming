class Cake:
    def __init__(self, flour, sugar, butter, eggs, bakingTemperature, bakingTime):
        self.flour = flour
        self.sugar = sugar
        self.butter = butter
        self.eggs = eggs
        self.bakingTemperature = bakingTemperature
        self.bakingTime = bakingTime

    def bake(self):
        print(f'My baking time is {self.bakingTime} and I need to be baked in {self.bakingTemperature} degrees')


class ShortCake(Cake):
    def __init__(self, flour=195, sugar=130, butter=200, eggs=3, bakingTemperature=175, bakingTime=50):
        super().__init__(flour, sugar, butter, eggs, bakingTemperature, bakingTime)
        self.spices = []

    def spice(self, spices_list):
        for spices in spices_list:
            self.spices.append(spices)


def main():
    spongeCake = Cake(340, 130, 0, 4, 175, 30)
    spongeCake.bake()

    cognagCake = ShortCake()
    spices =[('cognac', '2 tsp'), ('vanillapod', '1')]
    cognagCake.spice(spices)
    cognagCake.bake()


if __name__ == '__main__':
    main()
