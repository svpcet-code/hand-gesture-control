import cv2
import mediapipe as mp
import actions

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Only 4 fingers (thumb ignored for stability)
finger_tips = [8, 12, 16, 20]
prev_finger_count = -1   # 🔥 IMPORTANT

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_count = 0

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark

        # ---- COUNT FINGERS (NO THUMB) ----
        for tip in finger_tips:
            if lm[tip].y < lm[tip - 2].y:
                finger_count += 1

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        # 🔥 ACTION ONLY IF COUNT CHANGED 🔥
        if finger_count != prev_finger_count:
            prev_finger_count = finger_count

            if finger_count == 4:        # open palm
                actions.play_pause()

            elif finger_count == 3:
                actions.next_track()

            elif finger_count == 2:
                actions.prev_track()

            elif finger_count == 1:
                actions.volume_mute()

            elif finger_count == 0:      # fist
                actions.close_app()

        cv2.putText(frame, f'Fingers: {finger_count}',
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
