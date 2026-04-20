first do: docker build -t image (image can be named anything)
run something like docker run -v ~/home/michael/OSproject/michael_logs:/app/logs image (<- this will be whatever you named image in building)
