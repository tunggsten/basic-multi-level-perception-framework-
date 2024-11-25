from network import *

import linecache

import pygame

pygame.init()

#display = pygame.display.set_mode((854, 480))
pygame.display.set_caption("MNIST")

pygame.font.init()

font = pygame.font.Font(None, 36)



def interpret_mnist(mnistDataIndex:int):
    data = linecache.getline("MNISTtrain.csv", mnistDataIndex + 1)
    data = data.split(",")
    
    inputs = []
    
    for element in data:
        inputs.append(int(element))
    
    expectedDigit = inputs.pop(0)
    
    expectedOutput = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    expectedOutput.insert(expectedDigit, 1)
    
    for i in range(len(inputs)):
        inputs[i] /= 255
    
    return [inputs, expectedOutput]
    
    

def display_mnist(outputData:list[int], location:tuple=(16, 16), pixelSize:int=8):
    writtenDigit = pygame.Surface((pixelSize * 28, pixelSize * 28 + 16))
    
    for row in range(28):
        for collumb in range(28):
            colour = outputData[row * 28 + collumb] * 255
            pygame.draw.rect(writtenDigit, (colour, colour, colour), pygame.Rect(collumb * pixelSize, (row * pixelSize + 16), pixelSize, pixelSize))
    
    writtenDigit.blit(font.render("Input:", True, (255, 255, 255)), (0, 0))
                             
    display.blit(writtenDigit, location)
    
def display_expected(expected:list[int]):
    pass
    


testDigit = interpret_mnist(14)
print(testDigit)

network = Network([784, 200, 100, 80, 10])

oldLearningRate = 0.1

for i in range(500):
    trainingInputs = []
    trainingOutputs = []
    
    for j in range(50):
        data = interpret_mnist(i * 50 + j)
        
        trainingInputs.append(data[0])
        trainingOutputs.append(data[1])
        
    network.train(trainingInputs, trainingOutputs, 0.01)
    
    print(f"\nFinished training cycle {i + 1}.")
    
    testData = interpret_mnist(i)
    network.generate_output(testData[0])

    output = network.get_output()
    guess = output.index(max(output))
    actual = testData[1].index(max(testData[1]))
    
    print(f"Prediction: {output} Expected: {testData[1]}. \nLoss is {network.get_ssr(testData[1])}")
    print(f"Predicted {guess}, expected {actual}. {"\nCorrect!" if guess == actual else f"\nIncorrect"}")
    
network.save_model_to_file("MNISTmodel.model")


'''
running = True

i = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    testDigit = interpret_mnist(i)

    i += 1
            
    display.fill((50, 150, 255))
            
    display_mnist(testDigit[0])
        
    pygame.display.flip()'''