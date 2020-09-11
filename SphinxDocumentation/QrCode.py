class QrCode:
    'This class examine the QrCode'
    @staticmethod
    def scan():
        '''
        This function is to set up the camera and scan Qr code.
        
        
        '''
        # initialize the video stream and allow the camera sensor to warm up
        print("Starting scanning QRcode...")
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)

        found = set()

        # loop over the frames from the video stream
        while True:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width = 400)

            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)

            # loop over the detected barcodes
            for barcode in barcodes:
                # the barcode data is a bytes object so we convert it to a string
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                # if the barcode text has not been seen before print it and update the set
                if barcodeData not in found:
                    print("Found book: "  +barcodeData)
                    found.add(barcodeData)
                    vs.stop()
                    return barcodeData
            
            # wait a little before scanning again
            time.sleep(1)
