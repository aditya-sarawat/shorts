from motivational_content import generate_motivational_content
import time

if __name__ == "__main__":
    count = 0
    while count < 10:
        generate_motivational_content()
        time.sleep(20)
        count += 1