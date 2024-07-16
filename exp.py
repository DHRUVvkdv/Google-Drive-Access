import time


def convert_to_time(timestamp):
    """Converts a numeric timestamp to a time object.

    Args:
        timestamp: The numeric timestamp to convert (e.g., 1721042223).

    Returns:
        A time object representing the converted timestamp.
    """
    time_in_seconds = float(timestamp)
    return time.localtime(time_in_seconds)


def main():
    """Converts a numeric timestamp to a human-readable format and prints it to the console."""
    timestamp = 1721118080
    converted_time = convert_to_time(timestamp)

    # Format the time for user-friendliness (consider time zone if needed)
    formatted_time = time.strftime(
        "%c", converted_time
    )  # Example: Tue Jul 16 00:03:43 2024

    print(f"The converted time is: {formatted_time}")
    # data = {
    #     "status": "success",
    #     "result": {
    #         "**1. Professor's Notes:**": "The professor's notes introduce the LEWAS system and its focus on explaining the system from the perspective of various questions. The notes mention that the system has 3 critical sensors located on the Stroubles Creek site, which include a sonde that measures water quality information, an argonaut that measures water quantity information, and a weather station that measures weather parameters. The system is solar-powered and uses the campus wireless network to transmit data to remote clients in real-time.\n\n",
    #         "**2. Professor's Sources:**": "* Lewas Systems Document.pdf (Page 3.0) - https://drive.google.com/file/d/1cSz4rP0UpiXyr1Hn4obzKnRy6zUJw-MG/view\n* Lewas Systems Document.pdf (Page 2.0) - https://drive.google.com/file/d/1cSz4rP0UpiXyr1Hn4obzKnRy6zUJw-MG/view\n* Lewas Systems Document.pdf (Page 15.0) - https://drive.google.com/file/d/1cSz4rP0UpiXyr1Hn4obzKnRy6zUJw-MG/view\n\n",
    #         "**3. Internet Notes:**": "The internet sources provide additional information about the LEWAS system, including its components and layout. The notes mention that the system includes environmental monitoring sensors and data collection, storage, and transmission hardware. The sensors and their data are used to monitor water quality, flow, and weather parameters.\n\n",
    #         "**4. Internet Sources:**": "* https://www.researchgate.net/figure/LEWAS-Field-Site-Layout_fig1_281685848\n* https://www.researchgate.net/figure/LEWAS-Lab-Physical-Layout_fig3_281685740\n* https://www.researchgate.net/figure/The-LEWAS-Operational-Diagram_fig1_281685661\n* http://lewas.ictas.vt.edu:9090/education/learning-tech\n* https://engineerfix.com/electrical/sensors/a-complete-guide-to-sensors/\n\n",
    #         "**5. Extra Sources:**": "* Lewas Systems Document.pdf (Page 1.0) - https://drive.google.com/file/d/1cSz4rP0UpiXyr1Hn4obzKnRy6zU\n",
    #     },
    # }
    # for key, value in data["result"].items():
    #     answer_text = f"{key}\n{value}\n"
    #     print(answer_text)


if __name__ == "__main__":
    main()
