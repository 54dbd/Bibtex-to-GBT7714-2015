<!-- Improved compatibility of back to top link: See: https://github.com/54dbd/Bibtex-to-gbt7714/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Patreon][patreon-shield]][patreon-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="https://i.ibb.co/zQvJf2L/Vector.png" alt="Vector" height="200"/>
  <h3 align="center">Bibtex to GB/T 7714-2015 Converter</h3>

  <p align="center">
    This project convert bibtex file into GBT7714 format
    <br />
    <a href="https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=7FA63E9BBA56E60471AEDAEBDE44B14C"><strong>Explore the GB/T 7714-2015 »</strong></a>
    <br />
    <a href="https://github.com/54dbd/Bibtex-to-gbt7714/issues">Report Bug</a>
  </p>
</div>




<!-- ABOUT THE PROJECT -->

## About The Project

This project aims to convert a bibtex file into GBT7714 format, which is a standard citation format used in Chinese
academic publications. By converting the bibtex file into GBT7714 format, it allows for easier integration of references
into Chinese academic papers.




<!-- GETTING STARTED -->

## Getting Started

This project runs on python 3.9+, lower version is not tested.

### Prerequisites

* python 3.9+
* poetry

### Installation

1. Clone the repo

  ```sh
    git clone https://github.com/54dbd/Bibtex-to-gbt7714-converter.git
  ```

2. Install poetry packages

  ```sh
   poetry install
  ```  

or

  ```sh
   pip install -r requirements.txt
  ```  

3. Run the converter script with the bibtex file as input:

  ```sh
   python main.py ./ref.bib
  ```

Replace ref.bib with the name of your bibtex file.


<!-- USAGE EXAMPLES -->

## Usage

For example, if you have a bibtex file ref.bib, you can run the following command to convert it to GBT7714 format:

  ```sh
  python convert.py ref.bib
  ```

<!-- ROADMAP -->

## Roadmap

- [x] Support arxiv format input
- [x] Support common format input
- [ ] Support all the existing format
- [ ] Deal every kind of media in different way specifically
- [ ] Multi-language input support
  - [x] English
  - [ ] Chinese(no tested, considering this project is used for converting international references into chinese
    academic reference format)

See the [open issues](https://github.com/54dbd/Bibtex-to-gbt7714/issues) for a full list of proposed features (and known
issues).



<!-- CONTRIBUTING -->

## Contributing

- 54dbd
- Freddie_1946

<!-- LICENSE -->

## License

Distributed under the GPL-3.0 License. See `LICENSE.txt` for more information.


[contributors-shield]: https://img.shields.io/github/contributors/54dbd/Bibtex-to-gbt7714.svg?style=for-the-badge

[contributors-url]: https://github.com/54dbd/Bibtex-to-gbt7714/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/54dbd/Bibtex-to-gbt7714.svg?style=for-the-badge

[forks-url]: https://github.com/54dbd/Bibtex-to-gbt7714/network/members

[stars-shield]: https://img.shields.io/github/stars/54dbd/Bibtex-to-gbt7714.svg?style=for-the-badge

[stars-url]: https://github.com/54dbd/Bibtex-to-gbt7714/stargazers

[issues-shield]: https://img.shields.io/github/issues/54dbd/Bibtex-to-gbt7714.svg?style=for-the-badge

[issues-url]: https://github.com/54dbd/Bibtex-to-gbt7714/issues

[license-shield]: https://img.shields.io/github/license/54dbd/Bibtex-to-gbt7714.svg?style=for-the-badge

[license-url]: https://github.com/54dbd/Bibtex-to-gbt7714/blob/master/LICENSE.txt

[patreon-shield]: https://img.shields.io/badge/-patreon-black.svg?style=for-the-badge&logo=patreon&colorB=555

[patreon-url]: https://patreon.com/ross376
