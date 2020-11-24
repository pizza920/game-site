using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class JavascriptHook : MonoBehaviour {

    [SerializeField] private MainLobby mainLobby;
    [SerializeField] private GameManager gameManager;

    public void CreateRoom( string roomName)
    {
        mainLobby.CreateRoom(roomName);
    }

    public void JoinRoom( string roomName)
    {
        MainLobby._selectedRoomToJoin = roomName;
        mainLobby.OnClickJoinButton();
    }

    public void JoinRandomRoom()
    {
        if (gameManager == null)
        {
            mainLobby.OnClickRandomButton();
        }
        else
        {
            gameManager.OnClickRandomButton();
        }
    }
      

    public void TestJson(string json) {
        JsonObject jsonObject = JsonUtility.FromJson<JsonObject>(json);
    }

    private void Update() {
        
    }

    public class JsonObject {
        public string name;
        public int age;
    }
}
