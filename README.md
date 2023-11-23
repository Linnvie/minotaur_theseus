# minotaur_theseus
Đề tài này sử dụng các công nghệ, kỹ thuật và quy trình sau để tiến hành nghiên cứu và xây dựng game Theseus and Minotaur 2D:
Ngôn ngữ: Ngôn ngữ lập trình Python, Java
Thư viện chính: Pygame, NetworkX
Database: Hệ quản trị cơ sở dữ liệu PostgeSQL

1)	Name : Minotaur and Theseus
2)	Brief description:
Trò chơi giải đố mê cung Theseus và Minotaur là một loại mê cung logic được thiết kế bởi Robert Abbott. Trong mê cung này, người chơi sẽ vào vai Vua Theseus của Athens đang cố gắng trốn thoát khỏi mê cung. Sử dụng các phím mũi tên để di chuyển Theseus. Ý tưởng là đưa Theseus đến lối ra mà không bị Minotaur ăn thịt. Đối với mỗi nước đi mà Theseus thực hiện, Minotaur sẽ thực hiện hai nước đi. Minotaur luôn cố gắng đến gần hơn với Theseus. Nếu Minotaur có thể di chuyển một hình vuông theo chiều ngang và đến gần Theseus hơn, Minotaur sẽ làm được điều đó. Nếu Minotaur không thể di chuyển theo chiều ngang thì sẽ cố gắng di chuyển theo chiều dọc.Nếu không có nước đi nào ở gần người chơi, Minotaur sẽ bỏ qua lượt chơi. Theseus cũng có thể bỏ qua một lượt nếu muốn. 
3)	Gameplay:
•	Dựa trên truyền thuyết  Hy Lạp cổ đại về Ariadne và Theseus.
•	Storyline:
Minotaur, một con quái vật nửa người nửa bò đã gieo rắc kinh hoàng cho toàn đảo Crete nên vua Minos ra lệnh cho Daedalus làm một mê cung để nhốt nó lại. Sau đó vua Minos của Crete đã giành chiến thắng trong cuộc chiến với người Athen và yêu cầu Athene phải hy sinh bảy chàng trai trẻ và bảy thiếu nữ cứ 9 năm 1 lần  cho Minotaur ăn thịt. Thấu hiểu sự bất bình này, hoàng tử Theseus liền tình nguyện là một trong những người chịu cống nạp. Trong game, người chơi sẽ vào vai Theseus, đang bị mắc kẹt trong Mê cung thần thoại, buộc phải chiến đấu với Minotaur hung dữ bằng cách tìm đường thoát khỏi mê cung trước khi bị Minotaur ăn thịt. Theseus sẽ đánh bại Minotaur khi thoát khỏi tất cả các mê cung vì làm cho Minotaur kiệt sức khi đuổi theo.
•	Phương thức chơi:
	Chơi bằng bàn phím : dùng 4 phím lên xuống trái phải để di chuyển Theseus đến ô bất kì, bấm phím cách để bỏ qua lượt, bấm phím Backspace để trở lại đầu màn game, bấm phím Shift để undo lại bước đi vừa thực hiện.
	Chơi bằng chuột: Bấm chuột phải vào các Button tương ứng trên màn hình để di chuyển Theseus
•	Quy tắc trò chơi và cách tính điểm:
	Logic trò chơi: Người chơi phải di chuyển Theseus đến được lối ra trước khi bị Minotaur bắt (người chơi di chuyển Theseus 1 bước, Minotaur sẽ di chuyển 2 bước theo quy luật  Minotaur luôn cố gắng đến gần hơn với Theseus. Nếu Minotaur có thể di chuyển một hình vuông theo chiều ngang và đến gần Theseus hơn, Minotaur sẽ làm được điều đó. Nếu Minotaur không thể di chuyển theo chiều ngang thì sẽ cố gắng di chuyển theo chiều dọc.Nếu không có nước đi nào ở gần người chơi, Minotaur sẽ bỏ qua lượt chơi). Vòng chơi kết thúc khi Theseus thoát khỏi mê cung hoặc Theseus bị bắt
	Mỗi vòng chơi có thời gian không giới hạn, có lưu lại số bước đi đến lúc thoát ra khỏi mê cung 
	Độ khó trò chơi tăng lên theo từng level
	Khi đã qua màn mới có thể mở khóa để chơi vòng tiếp theo, hoặc chơi lại để đạt được số bước đi là thấp nhất
	Mục tiêu trò chơi là hoàn thành xuất sắc thử thách của mỗi cấp độ với số bước đi là ít nhất
•	Trợ giúp: Sử dụng hint gợi ý là các bước đi đã được tính toán bằng thuật toán A* và BFS

