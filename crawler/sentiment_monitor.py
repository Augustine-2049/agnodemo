#!/usr/bin/env python3
"""
A股上市公司舆情监控爬虫
支持多个平台的舆情数据爬取
"""

import sys
import os
import logging
from datetime import datetime, timedelta
import pandas as pd

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from crawler.logger_config import create_logger
    from crawler.test_crawler import crawl_eastmoney_news
    from crawler.xueqiu_crawler import crawl_xueqiu_discussions, crawl_xueqiu_news
except ImportError:
    from logger_config import create_logger

class SentimentMonitor:
    """
    A股舆情监控类
    整合多个平台的舆情数据爬取
    """
    
    def __init__(self, logger=None):
        """
        初始化舆情监控器
        :param logger: 日志对象
        """
        if logger is None:
            self.logger = create_logger('sentiment_monitor', console_level=logging.WARNING)
        else:
            self.logger = logger
        
        # 支持的平台列表
        self.platforms = {
            'eastmoney': {
                'name': '东方财富',
                'description': '东方财富股吧讨论',
                'function': self._crawl_eastmoney
            },
            'xueqiu_discussions': {
                'name': '雪球讨论',
                'description': '雪球网个股讨论',
                'function': self._crawl_xueqiu_discussions
            },
            'xueqiu_news': {
                'name': '雪球新闻',
                'description': '雪球网个股新闻',
                'function': self._crawl_xueqiu_news
            }
        }
    
    def _crawl_eastmoney(self, stock_code, max_pages=5, days_limit=7):
        """爬取东方财富数据"""
        return crawl_eastmoney_news(stock_code, self.logger, max_pages, days_limit)
    
    def _crawl_xueqiu_discussions(self, stock_code, max_pages=5, days_limit=7):
        """爬取雪球讨论数据"""
        return crawl_xueqiu_discussions(stock_code, self.logger, max_pages, days_limit)
    
    def _crawl_xueqiu_news(self, stock_code, max_pages=3, days_limit=7):
        """爬取雪球新闻数据"""
        return crawl_xueqiu_news(stock_code, self.logger, max_pages, days_limit)
    
    def crawl_all_platforms(self, stock_code, platforms=None, max_pages=5, days_limit=7):
        """
        爬取所有平台的舆情数据
        :param stock_code: 股票代码
        :param platforms: 要爬取的平台列表，如果为None则爬取所有平台
        :param max_pages: 最大页数
        :param days_limit: 时间限制（天）
        :return: 字典，包含各平台的数据
        """
        if platforms is None:
            platforms = list(self.platforms.keys())
        
        results = {}
        
        self.logger.info(f"开始爬取股票 {stock_code} 的舆情数据")
        self.logger.info(f"目标平台: {[self.platforms[p]['name'] for p in platforms]}")
        
        for platform in platforms:
            if platform not in self.platforms:
                self.logger.warning(f"不支持的平台: {platform}")
                continue
            
            try:
                self.logger.info(f"正在爬取 {self.platforms[platform]['name']} 数据...")
                
                # 根据平台调整参数
                if platform == 'xueqiu_news':
                    pages = min(max_pages, 3)  # 新闻页数限制
                else:
                    pages = max_pages
                
                df = self.platforms[platform]['function'](stock_code, pages, days_limit)
                results[platform] = df
                
                self.logger.info(f"{self.platforms[platform]['name']} 爬取完成，获取 {len(df)} 条数据")
                
            except Exception as e:
                self.logger.error(f"爬取 {self.platforms[platform]['name']} 失败: {e}")
                results[platform] = pd.DataFrame()
        
        return results
    
    def save_results(self, stock_code, results, output_dir='logs'):
        """
        保存爬取结果
        :param stock_code: 股票代码
        :param results: 爬取结果字典
        :param output_dir: 输出目录
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        saved_files = []
        
        for platform, df in results.items():
            if not df.empty:
                filename = f"{output_dir}/{platform}_{stock_code}.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                saved_files.append(filename)
                self.logger.info(f"已保存 {self.platforms[platform]['name']} 数据到: {filename}")
        
        # 合并所有平台数据
        all_data = []
        for platform, df in results.items():
            if not df.empty:
                df_copy = df.copy()
                df_copy['platform'] = self.platforms[platform]['name']
                all_data.append(df_copy)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_filename = f"{output_dir}/combined_{stock_code}.csv"
            combined_df.to_csv(combined_filename, index=False, encoding='utf-8-sig')
            saved_files.append(combined_filename)
            self.logger.info(f"已保存合并数据到: {combined_filename}")
        
        return saved_files
    
    def get_platform_info(self):
        """获取支持的平台信息"""
        return self.platforms

def get_available_platforms():
    """
    获取可用的舆情监控平台信息
    :return: 平台信息字典
    """
    platforms = {
        '东方财富': {
            'url': 'http://guba.eastmoney.com/',
            'description': '东方财富股吧，用户讨论活跃，信息更新及时',
            'data_type': ['股吧讨论', '新闻资讯'],
            'advantages': ['用户活跃度高', '信息更新快', '讨论质量较高'],
            'disadvantages': ['需要处理大量垃圾信息', '反爬虫机制较强']
        },
        '雪球': {
            'url': 'https://xueqiu.com/',
            'description': '雪球网，专业的投资社区，用户质量较高',
            'data_type': ['个股讨论', '新闻资讯', '研报'],
            'advantages': ['用户质量高', '专业性强', 'API接口相对稳定'],
            'disadvantages': ['数据量相对较少', '需要登录获取完整数据']
        },
        '同花顺': {
            'url': 'http://www.10jqka.com.cn/',
            'description': '同花顺股吧，用户基数大，信息丰富',
            'data_type': ['股吧讨论', '新闻资讯', '研报'],
            'advantages': ['用户基数大', '信息全面', '历史数据丰富'],
            'disadvantages': ['信息质量参差不齐', '反爬虫机制严格']
        },
        '新浪财经': {
            'url': 'https://finance.sina.com.cn/',
            'description': '新浪财经，权威的财经新闻平台',
            'data_type': ['新闻资讯', '股吧讨论'],
            'advantages': ['权威性强', '新闻质量高', '更新及时'],
            'disadvantages': ['讨论区活跃度一般', 'API接口有限']
        },
        '腾讯财经': {
            'url': 'https://finance.qq.com/',
            'description': '腾讯财经，综合性财经平台',
            'data_type': ['新闻资讯', '股吧讨论'],
            'advantages': ['平台稳定', '新闻质量好', '用户基数大'],
            'disadvantages': ['讨论区相对冷清', '数据获取难度大']
        },
        '网易财经': {
            'url': 'https://money.163.com/',
            'description': '网易财经，专业的财经资讯平台',
            'data_type': ['新闻资讯', '股吧讨论'],
            'advantages': ['新闻质量高', '更新及时', '界面友好'],
            'disadvantages': ['讨论区活跃度不高', '数据获取受限']
        },
        '金融界': {
            'url': 'http://www.jrj.com.cn/',
            'description': '金融界，专业的金融资讯平台',
            'data_type': ['新闻资讯', '研报', '股吧讨论'],
            'advantages': ['专业性强', '研报质量高', '数据全面'],
            'disadvantages': ['用户活跃度一般', '反爬虫机制严格']
        },
        '和讯网': {
            'url': 'http://www.hexun.com/',
            'description': '和讯网，老牌财经网站',
            'data_type': ['新闻资讯', '股吧讨论'],
            'advantages': ['历史数据丰富', '新闻质量稳定'],
            'disadvantages': ['用户活跃度下降', '更新频率较低']
        },
        '证券时报网': {
            'url': 'http://www.stcn.com/',
            'description': '证券时报网，权威证券媒体',
            'data_type': ['新闻资讯', '研报'],
            'advantages': ['权威性强', '新闻质量高', '官方背景'],
            'disadvantages': ['讨论功能有限', '数据获取难度大']
        },
        '中国证券网': {
            'url': 'http://www.cnstock.com/',
            'description': '中国证券网，官方证券媒体',
            'data_type': ['新闻资讯', '研报'],
            'advantages': ['官方权威', '信息准确', '更新及时'],
            'disadvantages': ['用户互动少', '数据获取受限']
        }
    }
    
    return platforms

def main():
    """主函数"""
    # 创建日志管理器
    logger = create_logger('sentiment_monitor', console_level=logging.WARNING)
    logger.info("=" * 80)
    logger.info("A股舆情监控系统启动")
    logger.info("=" * 80)
    
    # 创建舆情监控器
    monitor = SentimentMonitor(logger)
    
    # 测试股票代码
    test_codes = ['002594', '300474', '600036']
    
    # 显示支持的平台信息
    platforms_info = get_available_platforms()
    logger.info("可用的舆情监控平台:")
    for name, info in platforms_info.items():
        logger.info(f"  {name}: {info['description']}")
        logger.info(f"    数据类型: {', '.join(info['data_type'])}")
        logger.info(f"    优势: {', '.join(info['advantages'])}")
    
    # 爬取数据
    for code in test_codes:
        logger.info(f"\n开始监控股票 {code} 的舆情...")
        
        # 爬取所有平台数据
        results = monitor.crawl_all_platforms(code, max_pages=3, days_limit=7)
        
        # 保存结果
        saved_files = monitor.save_results(code, results)
        
        # 统计结果
        total_items = sum(len(df) for df in results.values() if not df.empty)
        logger.info(f"股票 {code} 舆情监控完成，共获取 {total_items} 条数据")
        logger.info(f"保存文件: {', '.join(saved_files)}")
    
    logger.info("\n" + "=" * 80)
    logger.info("舆情监控完成")
    logger.info("=" * 80)

if __name__ == "__main__":
    main() 