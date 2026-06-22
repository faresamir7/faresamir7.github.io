# Single source of truth for Resume + CV.
# Timeline follows the LinkedIn-generated resume (per user direction).

CONTACT = {
    "name": "Fares Amir Hassen",
    "title": "Technical Account Manager",
    "email": "faresamir7@gmail.com",
    "phone": "+216 54 522 599",
    "location": "Ariana, Tunisia",
    "linkedin_url": "https://www.linkedin.com/in/fares-amir-hassen-4913951b7",
    "linkedin_label": "linkedin.com/in/fares-amir-hassen",
    "github_url": "https://github.com/faresamir7",
    "github_label": "github.com/faresamir7",
    "website_url": "https://faresamir7.github.io",
    "website_label": "faresamir7.github.io",
}

SUMMARY = (
    "Technical Account Manager at Hewlett Packard Enterprise with a strong computer-science "
    "foundation and years of hands-on experience in wireless network engineering, cybersecurity, "
    "and enterprise infrastructure. Trusted technical advisor bridging enterprise customers and "
    "HPE engineering \u2014 turning complex wireless, storage, and security challenges into clear, "
    "proactive outcomes."
)

# Each role: title, company, dates, location, bullets (full set for CV; resume trims).
EXPERIENCE = [
    {
        "id": "tam",
        "title": "Technical Account Manager",
        "company": "Hewlett Packard Enterprise",
        "dates": "Jan 2026 \u2013 Present",
        "location": "Ariana, Tunisia",
        "bullets": [
            "Serve as the trusted technical advisor and primary HPE interface across the account, owning the technical relationship from escalation to resolution.",
            "Manage the delivery of contracted proactive support services, planning service improvements and staying accountable for defined service deliverables.",
            "Provide multi-technology support across HPE ProLiant servers, Synergy composable infrastructure, and 3PAR storage platforms.",
            "Troubleshoot and maintain SAN fabrics built on HPE and Brocade SAN switches, ensuring resilient storage connectivity.",
            "Support enterprise campus networking on HPE and Aruba switches, applying deep wireless and infrastructure expertise.",
            "Act as the bridge between customer teams and HPE engineering, translating complex technical issues into clear, proactive outcomes.",
        ],
    },
    {
        "id": "wne",
        "title": "Wireless Network Engineer",
        "company": "HPE Aruba Networking",
        "dates": "Mar 2023 \u2013 Dec 2025",
        "location": "Ariana, Tunisia",
        "bullets": [
            "Diagnosed wireless network issues involving Aruba Mobility Controllers, Masters, and Access Points across all OSI layers.",
            "Implemented and configured modern RADIUS authentication protocols for secure wireless access.",
            "Performed firmware upgrades on Aruba devices to ensure optimal performance and security.",
            "Provided remote technical support for Aruba AOS products, analyzing device logs to pinpoint and resolve disruptions.",
            "Assisted with AirWave and Central troubleshooting tools; configured Aruba Instant APs in enterprise environments.",
            "Documented network issues with detailed defect classification and tracked resolutions.",
            "Collaborated with cross-functional teams and kept customers updated throughout the resolution process.",
        ],
    },
    {
        "id": "nsi",
        "title": "Network Security Intern",
        "company": "3S Standard Sharing Software",
        "dates": "Mar 2022 \u2013 Sep 2022",
        "location": "Tunis, Tunisia",
        "bullets": [
            "Built a modular Python Flask web platform for centralized management and control of enterprise network nodes.",
            "Automated Cisco API integration with optimized, scalable calls for mass configuration of network infrastructure.",
            "Designed a secure authentication system with user role controls.",
            "Integrated a configuration database and conducted rigorous stability testing.",
        ],
    },
    {
        "id": "oxa",
        "title": "Network Technician Intern",
        "company": "OXAHOST",
        "dates": "Jun 2021 \u2013 Jul 2021",
        "location": "Tunis, Tunisia",
        "bullets": [
            "Created Tunisia's only CentOS mirror to support local infrastructure.",
            "Performed penetration testing on the company's new website and hosted services, including Zimbra and cPanel.",
            "Collaborated with web developers to harden website security ahead of launch.",
            "Audited and addressed a range of system and network security concerns.",
        ],
    },
    {
        "id": "biat20",
        "title": "Summer IT Intern",
        "company": "BIAT",
        "dates": "Aug 2020 \u2013 Sep 2020",
        "location": "Tunisia",
        "bullets": [
            "Assisted in designing, maintaining, and troubleshooting network infrastructure and devices (routers, switches, firewalls).",
            "Supported vulnerability assessments and penetration testing activities.",
            "Configured and managed network security tools (IDS/IPS, firewalls); analyzed logs for incident response.",
            "Configured secure remote access solutions (VPN, SSL) and collaborated on security best practices.",
        ],
    },
    {
        "id": "biat19",
        "title": "Summer Intern",
        "company": "BIAT",
        "dates": "Aug 2019 \u2013 Sep 2019",
        "location": "Tunisia",
        "bullets": [
            "Served as liaison between Backoffice and Frontoffice teams to streamline communication.",
            "Coordinated tasks and managed client requests, ensuring smooth information flow.",
            "Improved cross-team collaboration and overall workflow efficiency.",
        ],
    },
]

EDUCATION = [
    {
        "institution": "ESPRIT \u2014 \u00c9cole Sup\u00e9rieure Priv\u00e9e d'Ing\u00e9nierie et de Technologies",
        "degree": "Engineer's Degree (Dipl\u00f4me d'Ing\u00e9nieur, Master's level), Network Infrastructure and Data Security",
        "dates": "2017 \u2013 2022",
        "location": "Ariana, Tunisia",
    },
]

CERTIFICATIONS = [
    {"name": "CompTIA Network+ ce", "issuer": "CompTIA", "date": "Jan 2023", "note": "Expired Jan 2026"},
    {"name": "CIC NIST/NICE Framework", "issuer": "Palo Alto Networks Cybersecurity Academy", "date": "Nov 2021", "note": ""},
    {"name": "Jr Penetration Tester Learning Path", "issuer": "TryHackMe", "date": "Dec 2022", "note": ""},
    {"name": "System Administration and IT Infrastructure Services", "issuer": "Google", "date": "Nov 2020", "note": ""},
    {"name": "Cybersecurity and the X-Factor", "issuer": "University System of Georgia", "date": "Nov 2020", "note": ""},
    {"name": "Detecting and Mitigating Cyber Threats & Attacks", "issuer": "University of Colorado System", "date": "Nov 2020", "note": ""},
]

SKILLS = {
    "Technologies": [
        "HPE ProLiant", "HPE Synergy", "HPE 3PAR", "HPE & Brocade SAN switches",
        "HPE & Aruba switches", "Aruba AOS 8", "Aruba Instant APs", "Cisco",
        "RADIUS", "Python", "Shell scripting", "Wireshark",
    ],
    "Domains": [
        "Wireless network design", "RF technology & coverage planning",
        "Network troubleshooting (all OSI layers)", "SAN / storage infrastructure",
        "Server deployment", "Cybersecurity & penetration testing",
        "Packet analysis", "Automation", "Authentication",
    ],
    "Professional": [
        "Technical account management", "Client relationship management",
        "Cross-functional collaboration", "Technical documentation",
    ],
}

# Languages (confirmed by the candidate).
LANGUAGES = [
    {"language": "Arabic", "level": "Native"},
    {"language": "English", "level": "Bilingual proficiency"},
    {"language": "French", "level": "Professional working proficiency"},
    {"language": "Japanese", "level": "Beginner (conversational; limited reading)"},
]

INTERESTS = ["Cooking", "Gaming", "Gardening", "Plastic models", "Travelling", "Collecting", "3D modelling"]
