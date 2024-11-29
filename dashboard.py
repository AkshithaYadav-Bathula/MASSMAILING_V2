import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aks",  # Adjusted for your environment
        database="massmailing"
    )

def get_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            COUNT(*) AS total_sent,
            SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS total_delivered,
            SUM(CASE WHEN status = 'Landed in Inbox' THEN 1 ELSE 0 END) AS landed_inbox,
            SUM(CASE WHEN status = 'Landed in Spam' THEN 1 ELSE 0 END) AS landed_spam
        FROM email_status;
    """)
    stats = cursor.fetchone()
    cursor.close()
    conn.close()

    return {
        'total_sent': stats['total_sent'],
        'total_delivered': stats['total_delivered'],
        'landed_inbox': stats['landed_inbox'],
        'landed_spam': stats['landed_spam']
    }

def get_email_status():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM email_status")
    emails = cursor.fetchall()
    cursor.close()
    conn.close()

    return emails
