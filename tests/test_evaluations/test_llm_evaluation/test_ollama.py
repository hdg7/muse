import os

from pytest import mark

from muse.evaluation import OllamaMetric


@mark.skipif(os.getenv("SKIP_INTENSIVE_TESTS") == "true", reason="Skipping long tests")
def test_ollama_metric_single():
    ollama_metric = OllamaMetric({})
    result = ollama_metric.evaluate(
        [
            """Debian is a stable, versatile, and community-driven Linux distribution. It is known for its commitment to free and open-source software, reliability, and wide range of software packages. Debian has played a significant role in shaping the Linux ecosystem and is a popular choice for both personal and professional use."""
        ],
        reference_text=[
            """Debian: A Foundation for the Linux World
Debian is a venerable and widely respected Linux distribution, renowned for its stability, versatility, and commitment to free and open-source software. Founded in 1993 by Ian Murdock, Debian has grown into a cornerstone of the Linux ecosystem, serving as a foundation for numerous other distributions and powering a vast array of devices and systems.
Core Principles and Philosophy:
At the heart of Debian lies a steadfast adherence to its founding principles:
-Freedom: Debian is dedicated to promoting software freedom, ensuring that users have the right to run, copy, distribute, study, modify, and improve the software they use.
-Community: Debian is a community-driven project, relying on the contributions of thousands of volunteers worldwide. This collaborative approach fosters innovation, diversity, and a strong sense of ownership among its users.
-Stability: Debian prioritizes stability and reliability, ensuring that its releases are thoroughly tested and well-supported. This focus on stability makes Debian a popular choice for servers, desktops, and embedded systems.
-Variety: Debian offers a wide range of software packages, catering to diverse needs and preferences. From desktop environments to server applications, Debian has something to offer everyone.
Key Features and Benefits:
-Stability: Debian's reputation for stability is well-earned. Its releases undergo rigorous testing and are supported for an extended period, making them suitable for mission-critical systems.
-Versatility: Debian can be customized to suit a wide range of use cases, from personal desktops to enterprise servers. Its modular architecture allows users to select only the components they need.
-Security: Debian maintains a strong commitment to security, providing regular updates and patches to address vulnerabilities. The Debian Security Tracker is a valuable resource for staying informed about security issues.
-Community Support: Debian benefits from a large and active community, providing extensive documentation, forums, and mailing lists for support and collaboration.
-Wide Range of Software: Debian's package repositories offer a vast selection of software, including popular applications, development tools, and system utilities.
-Hardware Compatibility: Debian supports a wide range of hardware architectures, making it compatible with various devices and systems.
Debian's Impact on the Linux Ecosystem:
Debian has played a pivotal role in shaping the Linux ecosystem. It has served as a model for other distributions, influencing their design, packaging systems, and community structures. Debian's commitment to stability and reliability has helped to solidify Linux's reputation as a robust and dependable operating system.
In conclusion, Debian is a cornerstone of the Linux world, offering a stable, versatile, and community-driven platform for users of all levels. Its adherence to free and open-source principles, coupled with its focus on stability and security, has made Debian a trusted choice for individuals and organizations alike.
"""
        ],
    )
    print(result)

    for key_fact in result["ollama"][0]["key_fact_correspondence"]:
        print(key_fact)
