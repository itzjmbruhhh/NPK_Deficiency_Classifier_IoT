from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import LeafSample, SoilSample, Prediction
from .serializers import LeafSampleSerializer, SoilSampleSerializer, PredictionSerializer
from .utils import predict_image, preprocess_image
import serial
from .serial_connection import SerialConnection

@api_view(['GET'])
def dashboard_view(request):
    leaf_samples = LeafSample.objects.all()
    soil_samples = SoilSample.objects.all()
    predictions = Prediction.objects.all()

    leaf_samples_serializer = LeafSampleSerializer(leaf_samples, many=True)
    soil_samples_serializer = SoilSampleSerializer(soil_samples, many=True)
    predictions_serializer = PredictionSerializer(predictions, many=True)

    return Response({
        "leaf_samples": leaf_samples_serializer.data,
        "soil_samples": soil_samples_serializer.data,
        "predictions": predictions_serializer.data,
    })

@api_view(['POST'])
def predict_view(request):
    if request.method == "POST":
        if "fileImage" not in request.FILES:
            return Response({"success": False, "error_message": "No image file provided."}, status=400)

        uploaded_file = request.FILES["fileImage"]
        
        try:
            # Preprocess the image
            img_array = preprocess_image(uploaded_file)

            # Get prediction from the model
            prediction_result, confidence = predict_image(img_array)

            return Response({
                "success": True,
                "prediction": prediction_result,
                "confidence": round(confidence * 100, 2),
            })
        except ValueError as e:
            return Response({"success": False, "error_message": str(e)}, status=500)
    
    return Response({"success": False, "error_message": "Invalid request method"}, status=405)

arduino = SerialConnection(port="COM3", baudrate=4800, timeout=1)  # Persistent connection

@api_view(['GET'])
def arduino_data(request):
    try:
        data_lines = arduino.read_lines(3)  # Read sensor data
        print("Data lines read from Arduino:", data_lines)  # Debug statement

        sensor_data = {}
        for line in data_lines:
            if "Nitrogen:" in line:
                sensor_data["Nitrogen"] = line.split(":")[1].strip().replace(" mg/kg", "")
            elif "Phosphorus:" in line:
                sensor_data["Phosphorus"] = line.split(":")[1].strip().replace(" mg/kg", "")
            elif "Potassium:" in line:
                sensor_data["Potassium"] = line.split(":")[1].strip().replace(" mg/kg", "")

        print("Parsed sensor data:", sensor_data)  # Debug statement
        return Response({"sensor_data": sensor_data})

    except Exception as e:
        print("Error fetching sensor data:", str(e))  # Debug statement
        return Response({'error': str(e)}, status=500)