from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

"""
后端启动文件，建立数据库连接，提供新闻分析的数据，需要先运行此程序，建立前后端连接，再运行index.html

"""

app = Flask(__name__)
# 修改CORS配置，允许所有来源
CORS(app, origins="*", supports_credentials=True)

# 使用数据库连接
engine = create_engine('mysql+pymysql://root:qwer123123@localhost:3306/tushare_news_db')


@app.route('/api/news', methods=['GET'])
def get_news():
    start_date = request.args.get('start_date', '2025-05-12')
    end_date = request.args.get('end_date', '2025-05-12')

    # 直接从analysis_results表中按日期查询数据
    sql = f"SELECT * FROM analysis_results WHERE date BETWEEN '{start_date}' AND '{end_date}'"
    
    try:
        # 执行查询
        df = pd.read_sql(sql, engine)
        
        # 如果没有查询到结果，返回空列表
        if df.empty:
            return jsonify([])
            
        # 将DataFrame转换为JSON格式
        return jsonify(df.to_dict('records'))
    except Exception as e:
        # 记录错误并返回错误信息
        print(f"查询出错: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
