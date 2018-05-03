package com.example.deepak.bankingbot;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.EditText;

public class chumma extends AppCompatActivity {
EditText chumma;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chumma);
        chumma=(EditText)findViewById(R.id.editText9);
        System.out.println(chumma);
    }
}
