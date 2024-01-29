from machine import Pin, SPI
import network
import utime
import openapi

# W5x00 init
def init_ethernet(timeout=10):
    spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
    nic = network.WIZNET5K(spi, Pin(17), Pin(20))   # spi, cs, reset pin
    # DHCP
    nic.active(True)

    start_time = utime.ticks_ms()
    while not nic.isconnected():
        utime.sleep(1)
        if utime.ticks_ms() - start_time > timeout * 1000:
            raise Exception("Ethernet connection timed out.")
        print('Connecting ethernet...')

    print(f'Ethernet connected. IP: {nic.ifconfig()}')

def main():
    init_ethernet()

    while True:
        prompt = input("User: ")
        if prompt.lower() == "exit":  # 사용자가 'exit' 입력 시 루프 종료
            print("Exiting...")
            break

        try:
            response = openapi.send_prompt_to_gemini(prompt)  # Gemini API 호출
            print("Gemini: ", response)
        except Exception as e:
            print("Error: ", e)

if __name__ == "__main__":
    main()
