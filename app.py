import streamlit as st
import chess
import chess.pgn
import requests
import io

st.set_page_config(page_title="محلل مباريات الشطرنج الذكي", page_icon="♟️️")

st.title("♟️ محلل مباريات الشطرنج الذكي")

username = st.text_input("أدخل اسم المستخدم على Chess.com:")

if st.button("جلب وتحليل آخر مباراة"):
    if username:
        try:
            # جلب الأرشيف الأخير للمستخدم من Chess.com
            archives_url = f"https://api.chess.com/pub/player/{username}/games/archives"
            res = requests.get(archives_url, headers={"User-Agent": "ChessAnalyzerApp"})
            archives = res.json().get("archives", [])
            
            if not archives:
                st.error("لم يتم العثور على مباريات لهذا المستخدم.")
            else:
                # جلب أحدث شهر من المباريات
                latest_archive = archives[-1]
                games_res = requests.get(latest_archive, headers={"User-Agent": "ChessAnalyzerApp"})
                games = games_res.json().get("games", [])
                
                if not games:
                    st.error("لا توجد مباريات مسجلة في هذا الشهر.")
                else:
                    latest_game = games[-1]
                    pgn_text = latest_game.get("pgn", "")
                    
                    if pgn_text:
                        pgn_io = io.StringIO(pgn_text)
                        game = chess.pgn.read_game(pgn_io)
                        board = game.board()
                        
                        st.subheader("تفاصيل آخر مباراة:")
                        st.write(f"**الأبيض:** {game.headers.get('White', 'غير معروف')}")
                        st.write(f"**الأسود:** {game.headers.get('Black', 'غير معروف')}")
                        st.write(f"**النتيجة:** {game.headers.get('Result', 'غير معروف')}")
                        
                        st.markdown("---")
                        st.subheader("حركات المباراة:")
                        moves_list = list(game.mainline_moves())
                        st.write(f"إجمالي عدد الحركات: {len(moves_list)}")
                        
                        # عرض الرقعة النهائية
                        for move in moves_list:
                            board.push(move)
                            
                        st.write("رقعة الشطرنج في نهاية المباراة:")
                        st.text(str(board))
                    else:
                        st.error("تعذر جلب تفاصيل المباراة (PGN).")
        except Exception as e:
            st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
    else:
        st.warning("يرجى إدخال اسم المستخدم أولاً.")
