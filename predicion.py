import os
import segmentation
import joblib

current_dir = os.path.dirname(os.path.realpath(__file__))
model_dir = os.path.join(current_dir, "models/svc/svc.pk1")
model = joblib.load(model_dir)

classification_result = []

# Use the model to read the character images from the character list
for each_character in segmentation.characters:
    each_character = each_character.reshape(1, -1)
    result = model.predict(each_character)
    classification_result.append(result)

# Print the results of the classification process
print(classification_result)

# Display the predicted value
plate_string = ""
for eachPredict in classification_result:
    plate_string += eachPredict[0]

print(plate_string)

# Order and display the predicted value using the column_list
column_list_copy = segmentation.column_list[:]
segmentation.column_list.sort()
rightplace_string = ""
for each in segmentation.column_list:
    rightplace_string += plate_string[column_list_copy.index(each)]

print(rightplace_string)