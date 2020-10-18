import torch
from torchvision import models
from torchvision import transforms
from PIL import Image

resnet = models.resnet101(pretrained=True)

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])


def predict(image_path):
    img = Image.open(image_path)
    img.show()
    img_t = preprocess(img)
    batch_t = torch.unsqueeze(img_t, 0)

    resnet.eval()
    result = resnet(batch_t)

    with open('/Users/tomaye/Desktop/PersonalProjects/PytorchPlaying/data/imagenet_classes.txt') as f:
        labels = [line.strip() for line in f.readlines()]

    percentage = torch.nn.functional.softmax(result, dim=1)[0] * 100
    _, indices = torch.sort(result, descending=True)
    return [(labels[idx], percentage[idx].item()) for idx in indices[0][:5]]


print(predict("/Users/tomaye/Desktop/PersonalProjects/PytorchPlaying/data/RandomImages/dogs.jpg"))
