# -*- coding: utf-8 -*-
"""Translations for localized Resume/CV PDFs (FR, AR, JA).

English lives in data.py. Each language provides:
  - section headings (ui)
  - summary
  - per-role title + bullets (keyed by EXPERIENCE id)
  - dates (localized month names), locations
  - education, certifications, skills labels+values, languages, interests
Brand/proper nouns (HPE, Aruba, Python, company names) stay as-is.
"""

T = {
    "fr": {
        "ui": {
            "summaryHead": "Profil professionnel",
            "expHead": "Expérience professionnelle",
            "eduHead": "Formation",
            "certHead": "Certifications",
            "skillsHead": "Compétences & expertise",
            "langHead": "Langues",
            "interestsHead": "Centres d'intérêt",
            "keySkillsHead": "Compétences clés",
            "resumeTitle": "CV",
            "cvTitle": "Curriculum Vitae",
            "present": "Présent",
            "issued": "Délivré",
            "expired": "Expiré",
            "generated": "Généré en 2026",
        },
        "title": "Technical Account Manager",
        "summary": (
            "Technical Account Manager chez Hewlett Packard Enterprise, doté d'une solide "
            "formation en informatique et de plusieurs années d'expérience en ingénierie des "
            "réseaux sans fil, en cybersécurité et en infrastructure d'entreprise. Conseiller "
            "technique de confiance faisant le lien entre les clients et l'ingénierie HPE — en "
            "transformant des défis complexes de réseaux, de stockage et de sécurité en résultats "
            "clairs et proactifs."
        ),
        "roles": {
            "tam": {
                "title": "Technical Account Manager",
                "bullets": [
                    "Conseiller technique de confiance et interlocuteur HPE principal du compte, responsable de la relation technique de l'escalade à la résolution.",
                    "Piloter la fourniture des services de support proactif contractuels, planifier les améliorations de service et garantir les livrables définis.",
                    "Assurer un support multi-technologies sur les serveurs HPE ProLiant, l'infrastructure composable Synergy et les plateformes de stockage 3PAR.",
                    "Diagnostiquer et maintenir les fabriques SAN basées sur les commutateurs HPE et Brocade, garantissant une connectivité de stockage résiliente.",
                    "Prendre en charge le réseau de campus d'entreprise sur les commutateurs HPE et Aruba, en mobilisant une expertise approfondie du sans-fil et de l'infrastructure.",
                    "Faire le lien entre les équipes clientes et l'ingénierie HPE, en traduisant des problèmes techniques complexes en résultats clairs et proactifs.",
                ],
            },
            "wne": {
                "title": "Ingénieur réseaux sans fil",
                "bullets": [
                    "Diagnostic des problèmes de réseau sans fil impliquant les contrôleurs de mobilité, masters et points d'accès Aruba, sur toutes les couches OSI.",
                    "Mise en œuvre et configuration de protocoles d'authentification RADIUS modernes pour un accès sans fil sécurisé.",
                    "Mises à niveau des firmwares des équipements Aruba pour des performances et une sécurité optimales.",
                    "Support technique à distance des produits Aruba AOS, résolution des problèmes de connectivité par analyse des journaux.",
                    "Utilisation des outils AirWave et Central ; configuration de points d'accès Aruba Instant en environnement d'entreprise.",
                    "Documentation des incidents avec classification détaillée et suivi des résolutions.",
                    "Collaboration avec des équipes pluridisciplinaires et information continue des clients tout au long de la résolution.",
                ],
            },
            "nsi": {
                "title": "Stagiaire en sécurité réseau",
                "bullets": [
                    "Développement d'une plateforme web modulaire en Python Flask pour la gestion et le contrôle centralisés des nœuds réseau d'entreprise.",
                    "Automatisation de l'intégration de l'API Cisco avec des appels optimisés et évolutifs pour la configuration de masse de l'infrastructure réseau.",
                    "Conception d'un système d'authentification sécurisé avec gestion des rôles utilisateurs.",
                    "Intégration d'une base de données de configuration et réalisation de tests de stabilité rigoureux.",
                ],
            },
            "oxa": {
                "title": "Stagiaire technicien réseau",
                "bullets": [
                    "Création du seul miroir CentOS disponible en Tunisie pour soutenir l'infrastructure locale.",
                    "Tests d'intrusion sur le nouveau site web de l'entreprise et les services hébergés, dont Zimbra et cPanel.",
                    "Collaboration avec les développeurs web pour renforcer la sécurité du site avant son lancement.",
                    "Audit et traitement de divers problèmes de sécurité système et réseau.",
                ],
            },
            "biat20": {
                "title": "Stagiaire d'été (informatique)",
                "bullets": [
                    "Participation à la conception, la maintenance et le dépannage de l'infrastructure et des équipements réseau (routeurs, commutateurs, pare-feux).",
                    "Soutien aux évaluations de vulnérabilités et aux activités de tests d'intrusion.",
                    "Configuration et gestion d'outils de sécurité réseau (IDS/IPS, pare-feux) ; analyse des journaux pour la réponse aux incidents.",
                    "Configuration d'accès distants sécurisés (VPN, SSL) et collaboration sur les bonnes pratiques de sécurité.",
                ],
            },
            "biat19": {
                "title": "Stagiaire d'été",
                "bullets": [
                    "Rôle de liaison entre les équipes back-office et front-office pour fluidifier la communication.",
                    "Coordination des tâches et gestion des demandes clients, garantissant une circulation fluide de l'information.",
                    "Amélioration de la collaboration inter-équipes et de l'efficacité des flux de travail.",
                ],
            },
        },
        "dates": {
            "tam": "Janv. 2026 – Présent", "wne": "Mars 2023 – Déc. 2025",
            "nsi": "Mars 2022 – Sept. 2022", "oxa": "Juin 2021 – Juill. 2021",
            "biat20": "Août 2020 – Sept. 2020", "biat19": "Août 2019 – Sept. 2019",
        },
        "locations": {
            "tam": "Ariana, Tunisie", "wne": "Ariana, Tunisie", "nsi": "Tunis, Tunisie",
            "oxa": "Tunis, Tunisie", "biat20": "Tunisie", "biat19": "Tunisie",
        },
        "education": [{
            "institution": "ESPRIT — École Supérieure Privée d'Ingénierie et de Technologies",
            "degree": "Diplôme d'ingénieur (niveau master), Infrastructure réseau et sécurité des données",
            "dates": "2017 – 2022", "location": "Ariana, Tunisie",
        }],
        "certifications": [
            {"name": "CompTIA Network+ ce", "issuer": "CompTIA", "date": "Janv. 2023", "note": "Expiré janv. 2026"},
            {"name": "CIC NIST/NICE", "issuer": "Palo Alto Networks Cybersecurity Academy", "date": "Nov. 2021", "note": ""},
            {"name": "Parcours Jr Penetration Tester", "issuer": "TryHackMe", "date": "Déc. 2022", "note": ""},
            {"name": "Administration système et services d'infrastructure informatique", "issuer": "Google", "date": "Nov. 2020", "note": ""},
            {"name": "La cybersécurité et le facteur X", "issuer": "University System of Georgia", "date": "Nov. 2020", "note": ""},
            {"name": "Détecter et atténuer les cybermenaces et attaques", "issuer": "University of Colorado System", "date": "Nov. 2020", "note": ""},
        ],
        "skills": {
            "Technologies": ["HPE ProLiant", "HPE Synergy", "HPE 3PAR", "Commutateurs SAN HPE et Brocade",
                             "Commutateurs HPE et Aruba", "Aruba AOS 8", "Points d'accès Aruba Instant",
                             "Cisco", "RADIUS", "Python", "Scripts shell", "Wireshark"],
            "Domaines": ["Conception de réseaux sans fil", "Technologie RF et planification de couverture",
                         "Dépannage réseau (toutes couches OSI)", "Infrastructure SAN / stockage",
                         "Déploiement de serveurs", "Cybersécurité et tests d'intrusion",
                         "Analyse de paquets", "Automatisation", "Authentification"],
            "Professionnel": ["Gestion de comptes techniques", "Gestion de la relation client",
                              "Collaboration interfonctionnelle", "Documentation technique"],
        },
        "languages": [
            {"language": "Arabe", "level": "Langue maternelle"},
            {"language": "Anglais", "level": "Bilingue"},
            {"language": "Français", "level": "Maîtrise professionnelle"},
            {"language": "Japonais", "level": "Débutant, conversation"},
        ],
        "interests": ["Cuisine", "Jeux vidéo", "Jardinage", "Maquettes", "Voyages", "Collection", "Modélisation 3D"],
    },

    "ar": {
        "rtl": True,
        "ui": {
            "summaryHead": "الملف المهني",
            "expHead": "الخبرة المهنية",
            "eduHead": "التعليم",
            "certHead": "الشهادات",
            "skillsHead": "المهارات والخبرات",
            "langHead": "اللغات",
            "interestsHead": "الاهتمامات",
            "keySkillsHead": "المهارات الأساسية",
            "resumeTitle": "السيرة الذاتية",
            "cvTitle": "السيرة الذاتية الكاملة",
            "present": "حتى الآن",
            "issued": "صدرت في",
            "expired": "انتهت في",
            "generated": "أُنشئت في 2026",
        },
        "title": "مدير حسابات تقني",
        "summary": (
            "مدير حسابات تقني في شركة Hewlett Packard Enterprise، يتمتع بخلفية قوية في علوم "
            "الحاسوب وسنوات من الخبرة في هندسة الشبكات اللاسلكية والأمن السيبراني والبنية التحتية "
            "للمؤسسات. مستشار تقني موثوق يربط بين العملاء وهندسة HPE — محوّلًا التحديات المعقدة "
            "في الشبكات والتخزين والأمن إلى نتائج واضحة واستباقية."
        ),
        "roles": {
            "tam": {
                "title": "مدير حسابات تقني",
                "bullets": [
                    "العمل كمستشار تقني موثوق وكنقطة اتصال رئيسية مع HPE للحساب، مع تولّي العلاقة التقنية من التصعيد حتى الحل.",
                    "إدارة تقديم خدمات الدعم الاستباقي المتعاقد عليها، وتخطيط تحسينات الخدمة وتحمّل مسؤولية المخرجات المحددة.",
                    "تقديم الدعم متعدد التقنيات عبر خوادم HPE ProLiant وبنية Synergy القابلة للتركيب ومنصات التخزين 3PAR.",
                    "تشخيص وصيانة شبكات التخزين SAN المبنية على محوّلات HPE وBrocade، وضمان اتصال تخزين مرن وموثوق.",
                    "دعم شبكات الحرم المؤسسي على محوّلات HPE وAruba، مع توظيف خبرة عميقة في الشبكات اللاسلكية والبنية التحتية.",
                    "العمل كحلقة وصل بين فرق العملاء وهندسة HPE، وترجمة المشكلات التقنية المعقدة إلى نتائج واضحة واستباقية.",
                ],
            },
            "wne": {
                "title": "مهندس شبكات لاسلكية",
                "bullets": [
                    "تشخيص مشكلات الشبكات اللاسلكية المتعلقة بوحدات التحكم في التنقل والماسترات ونقاط الوصول من Aruba عبر جميع طبقات OSI.",
                    "تطبيق وتهيئة بروتوكولات مصادقة RADIUS الحديثة لتأمين الوصول اللاسلكي.",
                    "إجراء ترقيات للبرامج الثابتة لأجهزة Aruba لضمان الأداء والأمان الأمثل.",
                    "تقديم الدعم التقني عن بُعد لمنتجات Aruba AOS، وحل مشكلات الاتصال عبر تحليل السجلات.",
                    "استخدام أدوات AirWave وCentral؛ وتهيئة نقاط وصول Aruba Instant في بيئات المؤسسات.",
                    "توثيق المشكلات بتصنيف مفصّل ومتابعة الحلول.",
                    "التعاون مع فرق متعددة التخصصات وإبقاء العملاء على اطلاع طوال عملية الحل.",
                ],
            },
            "nsi": {
                "title": "متدرب في أمن الشبكات",
                "bullets": [
                    "تطوير منصة ويب معيارية بلغة Python Flask للإدارة والتحكم المركزي في عُقد شبكات المؤسسات.",
                    "أتمتة تكامل واجهة Cisco API باستدعاءات محسّنة وقابلة للتوسّع للتهيئة الجماعية للبنية التحتية للشبكة.",
                    "تصميم نظام مصادقة آمن مع إدارة أدوار المستخدمين.",
                    "دمج قاعدة بيانات للتهيئة وإجراء اختبارات استقرار دقيقة.",
                ],
            },
            "oxa": {
                "title": "متدرب فني شبكات",
                "bullets": [
                    "إنشاء المرآة الوحيدة لنظام CentOS المتوفرة في تونس لدعم البنية التحتية المحلية.",
                    "إجراء اختبار اختراق لموقع الشركة الجديد والخدمات المستضافة بما في ذلك Zimbra وcPanel.",
                    "التعاون مع مطوري الويب لتعزيز أمن الموقع قبل إطلاقه.",
                    "تدقيق ومعالجة مختلف المخاوف الأمنية للنظام والشبكة.",
                ],
            },
            "biat20": {
                "title": "متدرب صيفي (تقنية المعلومات)",
                "bullets": [
                    "المساهمة في تصميم وصيانة واستكشاف أعطال البنية التحتية وأجهزة الشبكة (أجهزة التوجيه، المحوّلات، الجدران النارية).",
                    "دعم تقييمات الثغرات وأنشطة اختبار الاختراق.",
                    "تهيئة وإدارة أدوات أمن الشبكة (IDS/IPS، الجدران النارية)؛ وتحليل السجلات للاستجابة للحوادث.",
                    "تهيئة حلول وصول آمن عن بُعد (VPN، SSL) والتعاون في أفضل ممارسات الأمن.",
                ],
            },
            "biat19": {
                "title": "متدرب صيفي",
                "bullets": [
                    "العمل كحلقة وصل بين فرق المكتب الخلفي والمكتب الأمامي لتيسير التواصل.",
                    "تنسيق المهام وإدارة طلبات العملاء، وضمان تدفق سلس للمعلومات.",
                    "تحسين التعاون بين الفرق وكفاءة سير العمل.",
                ],
            },
        },
        "dates": {
            "tam": "يناير 2026 – حتى الآن", "wne": "مارس 2023 – ديسمبر 2025",
            "nsi": "مارس 2022 – سبتمبر 2022", "oxa": "يونيو 2021 – يوليو 2021",
            "biat20": "أغسطس 2020 – سبتمبر 2020", "biat19": "أغسطس 2019 – سبتمبر 2019",
        },
        "locations": {
            "tam": "أريانة، تونس", "wne": "أريانة، تونس", "nsi": "تونس العاصمة، تونس",
            "oxa": "تونس العاصمة، تونس", "biat20": "تونس", "biat19": "تونس",
        },
        "education": [{
            "institution": "ESPRIT — المدرسة الخاصة العليا للهندسة والتقنيات",
            "degree": "شهادة مهندس (بمستوى الماجستير)، البنية التحتية للشبكات وأمن البيانات",
            "dates": "2017 – 2022", "location": "أريانة، تونس",
        }],
        "certifications": [
            {"name": "CompTIA Network+ ce", "issuer": "CompTIA", "date": "يناير 2023", "note": "انتهت في يناير 2026"},
            {"name": "CIC NIST/NICE", "issuer": "أكاديمية Palo Alto Networks للأمن السيبراني", "date": "نوفمبر 2021", "note": ""},
            {"name": "مسار Jr Penetration Tester", "issuer": "TryHackMe", "date": "ديسمبر 2022", "note": ""},
            {"name": "إدارة الأنظمة وخدمات البنية التحتية لتقنية المعلومات", "issuer": "Google", "date": "نوفمبر 2020", "note": ""},
            {"name": "الأمن السيبراني وعامل X", "issuer": "University System of Georgia", "date": "نوفمبر 2020", "note": ""},
            {"name": "اكتشاف التهديدات والهجمات السيبرانية والتصدي لها", "issuer": "University of Colorado System", "date": "نوفمبر 2020", "note": ""},
        ],
        "skills": {
            "التقنيات": ["HPE ProLiant", "HPE Synergy", "HPE 3PAR", "محوّلات SAN من HPE وBrocade",
                         "محوّلات HPE وAruba", "Aruba AOS 8", "نقاط وصول Aruba Instant",
                         "Cisco", "RADIUS", "Python", "برمجة Shell", "Wireshark"],
            "المجالات": ["تصميم الشبكات اللاسلكية", "تقنية RF وتخطيط التغطية",
                         "استكشاف أعطال الشبكة (جميع طبقات OSI)", "البنية التحتية SAN / التخزين",
                         "نشر الخوادم", "الأمن السيبراني واختبار الاختراق",
                         "تحليل الحزم", "الأتمتة", "المصادقة"],
            "المهارات المهنية": ["إدارة الحسابات التقنية", "إدارة علاقات العملاء",
                                 "التعاون متعدد الوظائف", "التوثيق التقني"],
        },
        "languages": [
            {"language": "العربية", "level": "اللغة الأم"},
            {"language": "الإنجليزية", "level": "إتقان ثنائي اللغة"},
            {"language": "الفرنسية", "level": "إتقان مهني"},
            {"language": "اليابانية", "level": "مبتدئ (محادثة؛ قراءة محدودة)"},
        ],
        "interests": ["الطبخ", "الألعاب", "البستنة", "المجسّمات", "السفر", "جمع المقتنيات", "النمذجة ثلاثية الأبعاد"],
    },
}
