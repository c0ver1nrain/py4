import nltk
import string
import matplotlib.pyplot as plt
from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# 下载Gutenberg数据（如果尚未下载）
nltk.download('gutenberg')
nltk.download('punkt')

# 加载《爱丽丝漫游奇境记》的文本
alice_corpus = gutenberg.raw('carroll-alice.txt')

# 将文本分割成句子
sentences = sent_tokenize(alice_corpus)

# 预处理文本
def preprocess(text):
    text = ''.join([char for char in text if char not in string.punctuation and not char.isdigit()])
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

# 预处理句子
preprocessed_sentences = [preprocess(sentence) for sentence in sentences]

# 创建词频向量
vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
tf = vectorizer.fit_transform(preprocessed_sentences)

# 使用LatentDirichletAllocation进行主题建模
lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(tf)

# 获取特征名称
feature_names = vectorizer.get_feature_names()

# 可视化主题
def plot_top_words(model, feature_names, n_top_words, title):
    fig, axes = plt.subplots(1, 5, figsize=(15, 3), sharex=True)
    for topic_idx, topic in enumerate(model.components_):
        top_features_idx = topic.argsort()[:-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_idx]
        weights = topic[top_features_idx]
        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx + 1}", fontsize=12)
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', labelsize=10)
    plt.subplots_adjust(wspace=0.5, hspace=0.3)
    plt.suptitle(title, fontsize=16)
    plt.show()

n_top_words = 10
plot_top_words(lda, feature_names, n_top_words, "Topics in LDA model")
