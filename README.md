MSQCRF+ – A Multimodal Smart Query and Civic Resolution Framework
PhD Technical Documentation
Abstract
This research proposes a novel algorithmic framework, MSQCRF+, that enables a chatbot to process multimodal
Introduction
The MSQCRF+ framework is designed to enhance user interaction with civic services by leveraging advanced
System Architecture
The system architecture of MSQCRF+ consists of several key components:
1. Multimodal Input Handler: Accepts text, image, audio, and video inputs.
2. Voice Converter: Converts audio and video inputs to text using Google Speech API.
3. Image Classifier: Uses ResNet50 and cosine similarity to classify images.
4. Semantic Matcher: Matches user queries to NMC services using TF-IDF or BERT.
5. Web Scraper: Extracts relevant content from the NMC website and external platforms.
6. Complaint Logger: Captures live images and location for complaint registration.
7. Data Persistence: Stores training data and scraped content using Pickle and JSON.
Detailed Algorithmic Explanations
AI Techniques
The MSQCRF+ framework employs various AI techniques to enhance user interaction and service delivery:
- Natural Language Understanding (NLU): Interprets user queries and maps them to civic services.
- Decision Logic: Dynamically routes requests based on input type and content.
- Contextual Awareness: Adapts to user language and real-time content using web scraping and translation.
Machine Learning (ML)
The framework leverages pretrained models and feature-based classification:
- Transfer Learning: Uses ResNet50 pretrained on ImageNet for feature extraction.
- Instance-Based Learning: Employs cosine similarity for classification, similar to k-nearest neighbors (KNN).
- Incremental Learning: Stores new image features and labels for on-the-fly learning.
Deep Learning
Deep learning techniques are used for various tasks:
- Convolutional Neural Networks (CNNs): ResNet50 extracts 2048-dimensional feature vectors from images.
- Speech-to-Text: Google Speech API converts audio and video speech to text.
- Optional Enhancement: Integrate transformer models like BERT for semantic understanding of queries.
Computer Vision
Computer vision techniques are employed for image processing and classification:
- Image Preprocessing: Resizing, RGB conversion, and normalization.
- Feature Extraction: ResNet50 outputs feature vectors representing image content.
- Similarity-Based Classification: Uses cosine similarity for matching features.
- Live Camera Integration: Captures and classifies images in real-time.
Natural Language Processing (NLP)
NLP techniques are used for text matching and translation:
- Text Matching: Uses TF-IDF and cosine similarity to match user queries to services.
- Translation: Google Translate API converts queries to Marathi.
Web Automation and Scraping
Web scraping and automation techniques are used to extract dynamic content:
- Web Scraping: Uses BeautifulSoup and Requests to extract data from the NMC website.
- Web Automation: Selenium or Playwright for interacting with dynamic content.
- Data Augmentation: Enriches chatbot responses with real-world data.
Multimodal AI Integration
The framework integrates multiple AI techniques to handle diverse inputs:
- Multimodal Input Handling: Accepts and processes text, image, audio, and video.
- Unified Processing Pipeline: The voiceconverter function routes and processes inputs.
- Contextual Decision Making: Decides whether to classify an image, transcribe speech, or fetch service data.

Novel Contributions
The MSQCRF+ framework introduces several novel contributions:
- Unified Multimodal Input Pipeline: Handles text, image, audio, and video inputs in a single pipeline.
- Lightweight Image Classification: Uses cosine similarity for classification without retraining models.
- Real-Time Complaint Logging: Captures live images and location for complaint registration.
- Dynamic Content Enrichment: Integrates web scraping to provide real-time information.
- Multilingual Support: Uses translation to handle queries in multiple languages.

 
Component	Algorithm    / Purpose	Novelty                        /  Integration
Image Classification	 /ResNet50 (CNN) + Cosine Similarity	     /Classify complaint images	Lightweight, retraining-free classification
Speech Recognition	   /  Google Speech API	                     /Convert audio/video to text	Enables voice/video-based queries
Multimodal Input      /Fusion	Custom routing logic in voiceconverter()	/Handle text, image, audio, video	Unified input processing pipeline
Semantic Text Matching	/TF-IDF / Cosine Similarity             /Match user query to NMC services	Enables natural language understanding
Web Scraping	      / BeautifulSoup + Requests	                /Extract service URLs and descriptions from NMC	Keeps service list dynamically updated
Web Automation	    /Selenium 	                                /Navigate and extract from dynamic pages (e.g.,NMC website Facebook, YouTube)	Augments chatbot with real-world data
Translation	Google Translate API /	Translate queries to Marathi	/Supports multilingual interaction
Complaint Logging	  / Live camera + location capture	            /Register civic complaints	Real-time, location-aware issue reporting
Data Persistence	  /Pickle (for features), JSON (for URLs)      /Store training data and scraped content	Lightweight and easy to manage
 
 
