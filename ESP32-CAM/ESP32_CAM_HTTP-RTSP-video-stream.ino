#include "src/OV2640.h"
#include <WiFi.h>
#include <WebServer.h>
#include <WiFiClient.h>

#include "src/OV2640Streamer.h"
// #include "src/SimStreamer.h"
#include "src/CRtspSession.h"

#define ENABLE_WEBSERVER
#define ENABLE_RTSPSERVER

// Select camera model
//#define CAMERA_MODEL_WROVER_KIT
//#define CAMERA_MODEL_ESP_EYE
//#define CAMERA_MODEL_M5STACK_PSRAM
//#define CAMERA_MODEL_M5STACK_WIDE
#define CAMERA_MODEL_AI_THINKER
// #define CAMERA_MODEL_M5CAM

#include "camera_pins.h"

OV2640 cam;

#ifdef ENABLE_WEBSERVER
WebServer server(80);
#endif

#ifdef ENABLE_RTSPSERVER
WiFiServer rtspServer(8554);
#endif

#include "wifikeys.h"

#ifdef ENABLE_WEBSERVER
void handle_mjpeg(void)
{
  WiFiClient client = server.client();
  String response = "HTTP/1.1 200 OK\r\n";
  response += "Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n";
  server.sendContent(response);

  while (true) {
    if (!client.connected()) {
      Serial.println("No Client connected");
      break;
    }
    cam.run();
    response = "--frame\r\n";
    response += "Content-Type: image/jpeg\r\n\r\n";
    server.sendContent(response);

    client.write((char *)cam.getfb(), cam.getSize());
    server.sendContent("\r\n");
  }
}

void handle_jpg(void)
{
    WiFiClient client = server.client();

    cam.run();
    if (!client.connected())
    {
      return;
    }
    // String response = "HTTP/1.1 200 OK\r\n";
    // response += "Content-disposition: inline; filename=capture.jpg\r\n";
    // response += "Content-type: image/jpeg\r\n\r\n";
    // server.sendContent(response);
    server.setContentLength(cam.getSize());
    server.send(200, "image/jpeg");
    client.write((char *)cam.getfb(), cam.getSize());
}

void handle_not_found()
{
    String message = "Server is running!\n\n";
    message += "URI: ";
    message += server.uri();
    message += "\nMethod: ";
    message += (server.method() == HTTP_GET) ? "GET" : "POST";
    message += "\nArguments: ";
    message += server.args();
    message += "\n";
    server.send(200, "text/plain", message);
}
#endif

void setup()
{
    Serial.begin(115200);
    while (!Serial);            //wait for serial connection. 

    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_SVGA; // 800 X 600
    config.jpeg_quality = 12; 
    config.fb_count = 2;
  
    #if defined(CAMERA_MODEL_ESP_EYE)
      pinMode(13, INPUT_PULLUP);
      pinMode(14, INPUT_PULLUP);
    #endif
  
    cam.init(config);
    
    IPAddress ip;
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(F("."));
    }
    Serial.println("");
    ip = WiFi.localIP();
    Serial.println("WiFi connected");
    Serial.println(ip);


#ifdef ENABLE_WEBSERVER
    Serial.print("Stream Link: http://");
    Serial.println(ip);
    Serial.println("  /cam.jpg");
    Serial.println("  /cam.mjpeg");

    server.on("/cam.jpg", handle_jpg);
    server.on("/cam.mjpeg", handle_mjpeg);
    server.onNotFound(handle_not_found);
    server.begin();
#endif

#ifdef ENABLE_RTSPSERVER
    rtspServer.begin();
    Serial.print("Stream Link: rtsp://");
    Serial.print(ip);
    Serial.println(":8554/mjpeg/1");
#endif
}

CStreamer *streamer;
CRtspSession *session;
WiFiClient client;

static uint64_t last_time = esp_timer_get_time();

void loop()
{
  // Display WiFi signal level
  // Serial.print(ssid);
  // Serial.print(" Signal Level: ");
  // Serial.println(WiFi.RSSI());
#ifdef ENABLE_WEBSERVER
    server.handleClient();
#endif

#ifdef ENABLE_RTSPSERVER

    uint32_t msecPerFrame = 100;
    static uint32_t lastimage = millis();

    // If we have an active client connection, just service that until gone
    if(session) {
        session->handleRequests(0); // we don't use a timeout here,
        // instead we send only if we have new enough frames
        
        uint32_t now = millis();

        // session->broadcastCurrentFrame(now);
        if(now > lastimage + msecPerFrame || now < lastimage) { // handle clock rollover
            session->broadcastCurrentFrame(now);
            lastimage = now;

            // check if we are overrunning our max frame rate
            now = millis();
            if(now > lastimage + msecPerFrame)
                printf("warning exceeding max frame rate of %d ms\n", now - lastimage);
        }

        if(session->m_stopped) {
            delete session;
            delete streamer;
            session = NULL;
            streamer = NULL;
        }
    }
    else {
        client = rtspServer.accept();

        if(client) {
            Serial.println("New Client connected");
            streamer = new OV2640Streamer(&client, cam);  // streamer for UDP/TCP based RTP transport

            session = new CRtspSession(&client, streamer); // threads RTSP session and state
        }
    }
#endif
}
