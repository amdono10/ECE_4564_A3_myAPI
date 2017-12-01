# ECE_4564_A3_myAPI
Assignment 3 for ECE 4564 Network Applications

Our service is a "what if" grade simulator. The user must send a GET request to canvas at the following path:

'/calculator/api/v1/grades'

Which returns all of the classes that a user is enrolled in.

The user also has the option to get a single class from the path:

'calculator/api/v1/grades/<int:class_id>'

Where the class id is the course ID.

The user can send a post request to our service at the following path:

'/canvas/api/v1/send',

And they can input their desired "what-if" grade for the course.

Finally we have the path for the LED Pi.

'/LED?status=status&color=color&intenstity=intensity'

where status, color, and intensity are all used to control the LED