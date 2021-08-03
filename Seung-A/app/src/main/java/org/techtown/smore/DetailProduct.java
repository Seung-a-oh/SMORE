package org.techtown.smore;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;

public class DetailProduct extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail_product);

        Button ReviewButton = findViewById(R.id.ReviewButton);
        ReviewButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(DetailProduct.this,ProductReview.class);
                startActivity(intent);
            }
        });
//        for(int i=1; i<=4; i++){
//            ImageView imageView = ImageView();
//            String photo_name = "mamaforest_detailcut"+i;
//            imageView.setBackgroundResource(R.drawable.);
//        }
    }
}