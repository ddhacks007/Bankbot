package com.example.deepak.bankingbot;

import android.content.Intent;
import android.nfc.Tag;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.view.ContextThemeWrapper;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;


public class MainActivity extends AppCompatActivity {
private RequestQueue requestQueue;
    private StringRequest stringRequest;
    private String url;
    private EditText username;
    private EditText password;
    int count=0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        setContentView(R.layout.layout);
        username=(EditText)findViewById(R.id.name);
        password=(EditText)findViewById(R.id.password);

    }
    public void Verification(View v){
        String user=username.getText().toString();
        String pass=password.getText().toString();
        System.out.println(user);
        System.out.println(pass);
url="http://10.0.2.2:4666/login/"+user+"/"+pass;
        System.out.println(url);
requestQueue= Volley.newRequestQueue(this);
        stringRequest=new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
    Log.i("response",       response.toString());
                try{JSONObject jsonObject=new JSONObject(response.toString());
if(jsonObject.getString("result").equals("sucess".toString())){
printfunc();
}else {
                        printF();}
                }
            catch(Exception e){

            }
        }}, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.i("error",error.toString());

            }
        });

requestQueue.add(stringRequest);


    }
    public void moveToNExtActivity(View view){

        Intent intent=new Intent(this,Main2Activity.class);
        startActivity(intent);

    }

public void printfunc(){
username.setText("");
    password.setText("");
    Toast.makeText(this,"SuccessfullLogin",Toast.LENGTH_LONG).show();
}
public void printF(){
    username.setText("");
    password.setText("");
    Toast.makeText(this,"UnSuccessfullLogin",Toast.LENGTH_SHORT).show();

}
}
